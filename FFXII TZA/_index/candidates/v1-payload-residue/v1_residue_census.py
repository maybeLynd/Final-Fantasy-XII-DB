"""V-1: does any instruction reach the SavePayload residue spans by ANY of the payload's entry routes?

Question: the store tiles all 353,424 payload bytes; 13,953 of them are UNKNOWN, and 11,940 of those are three spans
(+0x1538 2,760 B, +0xC818 6,120 B, +0x5589C 3,060 B) with no censused access. census_savepayload.py (a18a57456)
tested them from ONE route, the active-buffer getter 002EF640. AA-5's accepted disposition for a payload gap asked
for all routes. Discriminator: an offset-tracked census seeded at EVERY entry this database records for the image:
  getters   002EF640 active / 002EF620 staging / 002EF630 submission -> buffer base (payload -0x200);
            002EF2B0 payload base (payload +0)
  slots     mov rX,[02092758] -> -0x200 ; [020927C0] -> +0x8000 ; [02EBF190] -> +0x4E48C
  absolute  a rip-relative operand or lea into any of the four image buffers (02164280 / 021BA940 / 02211000 /
            022676C0, 0x56690 each), whether an access or a formed pointer
Offsets are carried through lea/add/sub/mov and into direct callees' argument slots for six hops (the walk of
census_savepayload.py, generalised to several seeds). A load through a tracked pointer kills the offset.

Controls:
  K0 the type store's tiling of SavePayload closes at exactly 0x56490 with no gap (walked through embedded types and
     arrays of them); it reports bytes by confidence and the UNKNOWN bytes by owning type
  K1 the census lands in every documented region (PersistentFlagPayload, the battle-state mirror,
     ImageBackedStateBlock, BattleSystemState) and on WorldTransition's +0x1044 read
  K2 each seed kind finds at least one host (a route that finds nothing has earned no opinion)
  K3 the absolute route finds the two whole-image clears 002EF5F0 / 002EF650 (lea 02164280), payload -0x200
  K4 planted mutant: a synthetic access at payload +0xC900 through a getter-seeded register is reported
  K5 agreement: how many sites of the published access census (save-payload-accesses.tsv) this one reproduces, and
     that none of the published rows lies in a residue span
  K6 blind spot: a raw displacement sweep of every listed body for the tail's rare displacements, any base; its own
     control is the known buffer-relative lea rdx,[rax+0x4E68C] at 00229B81
  K7 the +0xC818 span's displacements (payload- or buffer-relative) inside any function the census reached, as a
     candidate list (these displacements are common elsewhere, so only census-reached bodies are listed)
Boundary (unchanged from the parent census): indirect calls are not followed; computed (index-register) offsets are
not tracked; a pointer cached in memory and reloaded is killed. Whole-image memcpy/memset by length are the bulk
route, which the field-map page's 2026-09-19 section already covers.
Usage: python v1_residue_census.py -> result.json beside this script.
"""
import collections, json, os, sys, pathlib
sys.path.insert(0, r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts")
import check_default_instance_writers as W  # noqa: E402
import capstone  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402

X = capstone.x86
HERE = pathlib.Path(__file__).resolve().parent
SIZE = 0x56490
GETTERS = {0x002EF640: -0x200, 0x002EF620: -0x200, 0x002EF630: -0x200, 0x002EF2B0: 0}
SLOTS = {0x02092758: -0x200, 0x020927C0: 0x8000, 0x02EBF190: 0x4E48C}
BUFFERS = (0x02164280, 0x021BA940, 0x02211000, 0x022676C0)
IMG = 0x56690
RESIDUE = [(0x1538, 2760, "unobservedSpan1538"), (0xC818, 6120, "unobservedSpanC818"),
           (0xE004, 60, "unobservedSpanE004"), (0x4E469, 3, "transitionMetaHole4E469"),
           (0x4E474, 4, "transitionMetaHole4E474"), (0x4E479, 7, "transitionMetaHole4E479"),
           (0x4E484, 4, "transitionMetaHole4E484"), (0x5589C, 3060, "unobservedTail5589C")]
REGIONS = [(0x0, 0x1538, "PersistentFlagPayload"), (0x2008, 23306, "battle-state mirror"),
           (0x8000, 18456, "ImageBackedStateBlock"), (0x4E48C, 29712, "BattleSystemState")]


def absolute(a):
    for b in BUFFERS:
        if b <= a < b + IMG:
            return a - b - 0x200
    return None


def walk(img, entry, seed, acc, fwd, kinds, planted=None):
    t = W.Taint(img)
    starts, blocks, succ = t._blocks(entry)
    if not starts:
        return
    size = img.sizes.get(entry, 0)
    state = {starts[0]: dict(seed)}
    work = collections.deque([starts[0]])
    n = 0
    while work and n < 20000:
        n += 1
        b = work.popleft()
        off = dict(state[b])
        for i in blocks[b]:
            m = i.mnemonic
            if planted and i.address == planted[0]:
                r = W.norm(planted[1])
                if r in off:
                    acc[off[r] + planted[2]].add((entry, i.address, "planted"))
            for o in i.operands:
                if o.type != X86_OP_MEM:
                    continue
                a = W.rip_target(i, o)
                if a is not None:
                    d = absolute(a)
                    if d is not None and -0x200 <= d < SIZE and m != "lea":
                        acc[d].add((entry, i.address, "absolute")); kinds["absolute"].add(entry)
                    continue
                mm = o.value.mem
                base = W.norm(mm.base)
                if base not in off or mm.index or m == "lea":
                    continue
                d = off[base] + mm.disp
                if -0x200 <= d < SIZE:
                    acc[d].add((entry, i.address, "tracked"))
            if m == "lea" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG \
                    and i.operands[1].type == X86_OP_MEM:
                mm = i.operands[1].value.mem
                d = W.norm(i.operands[0].reg)
                a = W.rip_target(i, i.operands[1])
                if a is not None and absolute(a) is not None:
                    off[d] = absolute(a); kinds["absolute-lea"].add(entry)
                    acc[off[d]].add((entry, i.address, "lea-absolute"))
                elif W.norm(mm.base) in off and not mm.index:
                    off[d] = off[W.norm(mm.base)] + mm.disp
                else:
                    off.pop(d, None)
                continue
            if m in ("add", "sub") and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG:
                d = W.norm(i.operands[0].reg)
                if d in off and i.operands[1].type == X86_OP_IMM:
                    off[d] += i.operands[1].imm if m == "add" else -i.operands[1].imm
                else:
                    off.pop(d, None)
                continue
            if m == "mov" and len(i.operands) == 2 and i.operands[0].type == X86_OP_REG:
                d = W.norm(i.operands[0].reg)
                s = i.operands[1]
                if s.type == X86_OP_REG and W.norm(s.reg) in off:
                    off[d] = off[W.norm(s.reg)]
                    continue
                a = W.rip_target(i, s) if s.type == X86_OP_MEM else None
                if a in SLOTS and i.operands[0].size == 8:
                    off[d] = SLOTS[a]; kinds["slot %08X" % a].add(entry)
                    continue
                off.pop(d, None)
                continue
            if m in ("call", "jmp") and i.operands and i.operands[0].type == X86_OP_IMM:
                tgt = i.operands[0].imm
                if not (entry <= tgt < entry + size) and tgt in img.sizes:
                    for k, ar in enumerate(W.ARG_REGS):
                        if ar in off:
                            fwd.add((tgt, k + 1, off[ar]))
                if m == "call":
                    off = {k: v for k, v in off.items() if k not in W.VOLATILE}
                    if tgt in GETTERS:
                        off[X.X86_REG_RAX] = GETTERS[tgt]; kinds["getter %08X" % tgt].add(entry)
                continue
            if m == "call":
                off = {k: v for k, v in off.items() if k not in W.VOLATILE}
                continue
            try:
                _r, w = i.regs_access()
            except capstone.CsError:
                w = []
            for r in w:
                off.pop(W.norm(r), None)
        for s in succ[b]:
            prev = state.get(s)
            if prev is None:
                state[s] = dict(off); work.append(s)
            else:
                merged = {k: v for k, v in prev.items() if off.get(k) == v}
                if merged != prev:
                    state[s] = merged; work.append(s)


def hosts(img):
    """every function holding a seed: a getter call, a slot load, or an absolute operand into a buffer."""
    out = []
    for e in sorted(img.sizes):
        for i in img.body(e):
            hit = False
            if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM \
                    and i.operands[0].imm in GETTERS:
                hit = True
            for o in i.operands:
                a = W.rip_target(i, o)
                if a is not None and (a in SLOTS or absolute(a) is not None):
                    hit = True
            if hit:
                out.append(e); break
    return out


def store_coverage():
    """K0: the type store's tiling of SavePayload, walked through embedded types and arrays of them. Rejects the
    register's stale reading ('~470 bytes mapped'): the tiling must close at exactly 0x56490 with no gap."""
    import re
    by = collections.defaultdict(list)
    for l in open(pathlib.Path(__file__).resolve().parents[2].parent / "_types" / "fields.tsv", encoding="utf-8"):
        c = l.rstrip("\r\n").split("\t")
        if len(c) >= 9 and c[0] != "type":
            by[c[0]].append(c)
    rung = collections.Counter(); unk = collections.Counter(); gaps = []

    def go(t, mult, base):
        cur = 0
        for r in sorted(by[t], key=lambda r: int(r[1], 16)):
            o = int(r[1], 16); n = int(r[2]) if r[2].isdigit() else 0
            if o > cur:
                gaps.append("%s+0x%X" % (t, cur))
            eff = max(0, o + n - cur) if o < cur else n
            cur = max(cur, o + n)
            ct = r[4].split("[")[0].strip()
            if ct in by and ct != t and n > 0:
                m = re.search(r"\[(\d+)\]", r[4])
                go(ct, mult * (int(m.group(1)) if m else 1), base + o); continue
            rung[r[7]] += eff * mult
            if r[7] == "UNKNOWN":
                unk[t] += eff * mult
        return cur
    end = go("SavePayload", 1, 0)
    return {"tiled_end": "0x%X" % end, "gaps": gaps, "bytes_by_confidence": dict(rung.most_common()),
            "unknown_bytes_by_type": dict(unk.most_common()), "closes": end == SIZE and not gaps
            and sum(rung.values()) == SIZE}


def main():
    k0 = store_coverage()
    img = W.Image()
    hs = hosts(img)
    acc = collections.defaultdict(set); fwd = set(); kinds = collections.defaultdict(set)
    for e in hs:
        walk(img, e, {}, acc, fwd, kinds)
    seen = set(fwd); work = collections.deque((x[0], x[1], x[2], 0) for x in fwd)
    while work:
        fn, slot, o, d = work.popleft()
        nf = set()
        walk(img, fn, {W.ARG_REGS[slot - 1]: o}, acc, nf, kinds)
        if d >= 6:
            continue
        for g in nf:
            if g not in seen and len(seen) < 40000:
                seen.add(g); work.append((g[0], g[1], g[2], d + 1))
    # K4: a planted access, payload +0xC900, via rax after the first getter call found in 002EF2B0's first caller
    pa = collections.defaultdict(set)
    probe = next(e for e in hs if e in kinds["getter 002EF640"])
    body = img.body(probe)
    k = next(j for j, i in enumerate(body) if i.mnemonic == "call" and i.operands[0].type == X86_OP_IMM
             and i.operands[0].imm == 0x002EF640)
    walk(img, probe, {}, pa, set(), collections.defaultdict(set),
         planted=(body[k + 1].address, X.X86_REG_RAX, 0xC900 + 0x200))
    k4 = any("planted" in x[2] for x in pa.get(0xC900, ()))
    res = {}
    for o, s, n in RESIDUE:
        hit = sorted(d for d in acc if o <= d < o + s)
        res[n] = {"offset": "0x%X" % o, "bytes": s, "offsets_touched": ["0x%X" % d for d in hit],
                  "sites": sorted({"%08X@%08X %s" % x for d in hit for x in acc[d]})[:40]}
    reg = {n: sum(1 for d in acc if o <= d < o + s) for o, s, n in REGIONS}
    # K5: agreement with the published field-map access census (save-payload-accesses.tsv): how many of its sites this
    # census reproduces, and whether ITS rows touch any residue span (they must not: the store rows say "no access")
    import csv
    pub = [r for r in csv.DictReader(open(pathlib.Path(__file__).resolve().parents[3] / "19-Save-Load-Settings" /
                                          "Save-Image-Layout-And-Pipeline" / "save-payload-accesses.tsv",
                                          encoding="utf-8"), delimiter="\t")]
    mine = {x[1] for v in acc.values() for x in v}
    k5_sites = sum(1 for r in pub if int(r["site"], 16) in mine)
    k5_pub_in_residue = [r["site"] + " " + r["disp"] for r in pub
                         if any(o <= int(r["disp"], 16) < o + s for o, s, _n in RESIDUE)]
    # K6: raw displacement sweep over every listed body for the payload tail's RARE displacements (payload-relative
    # 0x5589C..0x56490, buffer-relative 0x55A9C..0x56690), any base register: a candidate list, not an identity
    k6, k6_ctrl, c818 = [], False, []
    reached = {x[0] for v in acc.values() for x in v}
    for e in sorted(img.sizes):
        for i in img.body(e):
            for o in i.operands:
                if o.type == X86_OP_MEM and W.rip_target(i, o) is None:
                    d = o.value.mem.disp
                    if 0x5589C <= d < 0x56490 or 0x55A9C <= d < 0x56690:
                        k6.append("%08X@%08X %s %s" % (e, i.address, i.mnemonic, i.op_str))
                    if i.address == 0x00229B81 and d == 0x4E68C:
                        k6_ctrl = True          # the sweep sees a known buffer-relative displacement
                    if (0xC818 <= d < 0xE000 or 0xCA18 <= d < 0xE200) and e in reached:
                        c818.append("%08X@%08X %s %s" % (e, i.address, i.mnemonic, i.op_str))
    k3 = all(any(x[0] == f and x[2] == "lea-absolute" for x in acc.get(-0x200, ())) for f in (0x002EF5F0, 0x002EF650))
    out = {
        "K0_store_coverage": k0,
        "seed_hosts": len(hs), "triples": len(seen), "distinct_offsets": len(acc),
        "seed_kinds": {k: len(v) for k, v in sorted(kinds.items())},
        "residue": res, "K1_regions": reg, "K1_1044": 0x1044 in acc,
        "K3_whole_image_clears": k3, "K4_planted": k4,
        "K5_published_sites": len(pub), "K5_published_sites_reproduced": k5_sites,
        "K5_published_rows_in_residue": k5_pub_in_residue, "K6_tail_raw_displacement_candidates": k6,
        "K6_control_00229B81": k6_ctrl, "K7_C818_raw_displacements_in_census_reached_functions": c818,
    }
    out["controls_pass"] = bool(k0["closes"] and all(reg.values()) and out["K1_1044"] and k3 and k4 and k6_ctrl
                                and all(any(k.startswith(p) for k in kinds) for p in ("getter", "slot", "absolute")))
    (HERE / "result.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in out.items() if k != "residue"}, indent=1))
    for n, r in res.items():
        print(n, r["bytes"], len(r["offsets_touched"]), r["offsets_touched"][:10], r["sites"][:6])


if __name__ == "__main__":
    main()
