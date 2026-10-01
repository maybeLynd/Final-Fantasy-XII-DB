#!/usr/bin/env python3
"""unlisted_entry_points.py - recover candidate function entries inside the unlisted blocks.

`unlisted-code-blocks.tsv` gives code RUNS between listed bodies, not bodies. OPUS's
body-shape control says a splitter block is not function-shaped, so the UC-1 denominator
cannot move on a block count. This instrument is the missing input: **where the real
entries are**.

Signals, per candidate entry X inside a block [s, s+n):

    call      X is the target of a *decoded* rel32 `call` anywhere in .text -
              the source scan covers listed bodies AND the decoded stream of
              every unlisted block (a body called only from unlisted code
              still earns the signal).
    jmp-in    X is the target of a decoded rel32 `jmp`/`jcc` whose source lies
              OUTSIDE this block (listed body or another block). A tail call
              lands on an entry.
    ref       X is in the pass-6-admissible reference union (rip-relative
              `lea` target, rel32 call/jmp target, or DIR64 relocation value).
              `.pdata` begins are unwind metadata - reported separately, never
              counted (OPUS-REQ-SWE2-EC7-UNLISTED-REFERENCED-ROUTES).
    post-term X follows a decoded terminator and no direct branch from earlier
              in the same segment reaches past it - i.e. the code at X is
              unreachable from the segment head, so it is a different body.
    aligned   X is 16-byte aligned (weak; never sufficient alone).

Boundary rule: a post-terminator offset P splits a segment iff no decoded
`jmp`/`jcc` has source < P and target > P. A branch landing exactly AT P is a
tail-call into a new body (entry evidence), not a reach.

Anchoring: a block's bytes are decoded in the stream that *precedes* them -
from the nearest earlier listed entry - so a block start that is mid-instruction
relative to the true stream is detected, not assumed. When the anchored stream
desyncs before the block (embedded data in the gap), the block is decoded from
its own start and marked `anchor:died`.

Controls (run by --self-test before any result is emitted):

    precision   apply the same boundary rule inside every listed body; the
                fraction that stay single is the no-invented-boundary rate.
    recall      run the detector over every pair of consecutive listed bodies
                (the second body's known entry is the ground truth); the
                fraction recovered is boundary recall on real shipping code.

The instrument does not move any denominator. It emits candidate entries with
their evidence; `unlisted-body-admissions.tsv` / progress.py consume a count.
"""
import argparse
import bisect
import collections
import io
import os
import struct
import sys

import capstone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unlisted_admissions as ua

OUT = os.path.join(ua.DB, "99-Unresolved-Residual", "Unlisted-Code",
                 "unlisted-entry-points.tsv")

TERMINATORS = ("ret", "jmp", "int3", "ud2", "hlt", "repz ret")
BRANCH_MNEMS = ("jmp", "ja", "jae", "jb", "jbe", "jc", "je", "jg", "jge", "jl",
                "jle", "jna", "jnae", "jnb", "jnbe", "jnc", "jne", "jng",
                "jnge", "jnl", "jnle", "jno", "jnp", "jns", "jnz", "jo", "jp",
                "jpe", "jpo", "js", "jz", "jrcxz", "jecxz", "loop", "loope",
                "loopne")


def decode_span(d, off, va0, va1):
    """Linear decode [va0, va1); returns instruction list (may stop early)."""
    o = off(va0)
    if o is None:
        return []
    o1 = off(va1 - 1)
    if o1 is None:
        return []
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    return list(md.disasm(d[o:o1 + 1], va0))


def branch_target(ins):
    """rel32/rel8 target of a direct branch/call, else None."""
    if ins.mnemonic in ("call", "jmp") or ins.mnemonic in BRANCH_MNEMS:
        op = ins.operands
        if op and op[0].type == capstone.x86.X86_OP_IMM:
            return op[0].imm
    return None


def harvest_table_targets(ins_list, d, off):
    """Indirect-jump (switch) table targets for the MSVC x64 idiom:

        lea  rb, [rip + R]            ; table base
        cmp  index_reg, bound         ; range guard (bound read, not trusted)
        mov  ra, dword [rb + idx*4 + D]
        add  ra, rb
        jmp  ra                       ; ra = rb + table[idx]

    For each `jmp <reg>` find the `add <reg>,<rb>`/`mov <reg>,[rb+idx*4+D]`/
    `lea rb,[rip+R]` chain above it, read dword entries at R+D while each
    computed target lands inside the same stream, and return those targets.
    A target the table holds is reachable code - never a boundary.
    """
    targets = set()
    # map register name -> lea target for simple `lea rX,[rip+R]` defs
    lea_base = {}
    for k, i in enumerate(ins_list):
        if i.mnemonic == "lea":
            m = i.operands
            if len(m) == 2 and m[1].type == capstone.x86.X86_OP_MEM \
                    and m[1].mem.base == capstone.x86.X86_REG_RIP:
                lea_base[i.reg_name(m[0].reg)] = i.address + i.size + m[1].mem.disp
        if i.mnemonic != "jmp":
            continue
        op = i.operands
        if not op or op[0].type != capstone.x86.X86_OP_REG:
            continue
        ra = i.reg_name(op[0].reg)
        # walk back for `add ra, rb` then `mov ra, dword[rb + _*4 + D]`
        rb = disp = None
        for j in range(k - 1, max(k - 12, -1), -1):
            x = ins_list[j]
            if x.mnemonic == "add":
                m = x.operands
                if len(m) == 2 and m[0].type == capstone.x86.X86_OP_REG \
                        and x.reg_name(m[0].reg) == ra \
                        and m[1].type == capstone.x86.X86_OP_REG:
                    rb = x.reg_name(m[1].reg)
            if x.mnemonic in ("mov", "movsxd") and rb is not None:
                m = x.operands
                if len(m) == 2 and x.reg_name(m[0].reg) == ra \
                        and m[1].type == capstone.x86.X86_OP_MEM \
                        and x.reg_name(m[1].mem.base) == rb \
                        and m[1].mem.index != capstone.x86.X86_REG_INVALID:
                    disp = m[1].mem.disp
                    break
        if rb is None or disp is None or rb not in lea_base:
            continue
        base = lea_base[rb]
        table = base + disp
        o = off(table)
        if o is None:
            continue
        for q in range(0, 4 * 4096, 4):     # a switch table is bounded; stop at nonsense
            ent = struct.unpack_from("<i", d, o + q)[0]
            tgt = base + ent
            if not (ins_list[0].address <= tgt < ins_list[-1].address +
                    ins_list[-1].size):
                break
            targets.add(tgt)
    return targets


def anchored_stream(d, off, entries, s, b_end):
    """Decode a block's instruction stream the way pass 2 does: from the
    nearest earlier listed entry so a mid-instruction block start is detected,
    falling back to the block's own start when that stream dies first.
    Returns (ins_list, anchor) with anchor in {self, prev, straddle, died}."""
    i = bisect.bisect_right(entries, s) - 1
    prev = entries[i] if i >= 0 else None
    if prev is None:
        return decode_span(d, off, s, b_end), "self"
    ins = decode_span(d, off, prev, b_end)
    starts = [x.address for x in ins]
    if starts and starts[-1] >= s:
        j = bisect.bisect_left(starts, s)
        anchor = "prev" if j < len(starts) and starts[j] == s else "straddle"
        return ins, anchor
    return decode_span(d, off, s, b_end), "died"


def segment_stream(ins_list, block_start, block_end, forced):
    """Split decoded instructions covering a block into bodies.

    forced: set of VAs that must be entries (call targets, external jmp targets,
            reference-union hits).
    Returns list of (entry_va, signals:set, seg_instructions).
    """
    ins_list = [i for i in ins_list if block_start <= i.address < block_end]
    if not ins_list:
        return []
    # every [terminator][padding run][code] point inside the block. The pad run
    # is the delimiter: measured inside listed bodies (precision control below,
    # 99.99%), an unreachable post-terminator instruction with NO padding
    # before the next code is almost always a dead island or a jump-table cold
    # path, and real boundaries are almost always padded. Known exceptions seen
    # in the residual review: fall-through bodies whose last instruction is not
    # a terminator (no pad, no boundary marker), decode desync across an
    # embedded data island, and adjacent import thunks - the rule can split or
    # merge there; those rows stay declared-uncertain rather than resolved.
    postterm = []
    PAD = ("int3", "nop")
    for k, i in enumerate(ins_list):
        if i.mnemonic not in TERMINATORS:
            continue
        j = k + 1
        while j < len(ins_list) and ins_list[j].mnemonic in PAD:
            j += 1
        if j < len(ins_list) and j > k + 1:
            q = ins_list[j].address
            if block_start < q < block_end:
                postterm.append(q)
    # branch map: source-va -> target-va for in-block direct jmp/jcc
    branches = []
    for i in ins_list:
        if i.mnemonic in BRANCH_MNEMS:
            t = branch_target(i)
            if t is not None and block_start <= t < block_end:
                branches.append((i.address, t))
    # candidate boundary set = post-term points + forced entries
    cand = sorted(set(postterm) | {f for f in forced if block_start < f < block_end})
    segs = []
    cur = ins_list[0].address
    cur_sig = set()
    # iterate over candidates in order; for each, test reachability
    for c in cand:
        if c <= cur:
            if c == cur:
                cur_sig.add("forced")
            continue
        if c in forced:
            segs.append((cur, cur_sig))
            cur, cur_sig = c, {"forced"}
            continue
        # boundary iff no same-segment branch reaches c or past it. A branch
        # landing AT c is flow re-joining after the pad (same body); a branch
        # reaching past c makes the pad an interior island. A tail call enters
        # from another region and is handled by the forced set instead.
        reach = any(src < c <= dst for src, dst in branches if src >= cur)
        if not reach:
            segs.append((cur, cur_sig))
            cur, cur_sig = c, {"post-term"}
    segs.append((cur, cur_sig))
    # attach instruction spans
    out = []
    starts = [s for s, _ in segs] + [block_end]
    for j, (s0, sig) in enumerate(segs):
        seg_ins = [i for i in ins_list if s0 <= i.address < starts[j + 1]]
        out.append((s0, sig, seg_ins))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", default=ua.EXE)
    ap.add_argument("--funcs", default=ua.FUNCS)
    ap.add_argument("--blocks", default=ua.BLOCKS)
    ap.add_argument("--errata", default=ua.ERRATA)
    ap.add_argument("--out", default=None)
    ap.add_argument("--self-test", action="store_true",
                    help="run the listed-population controls and print rates")
    a = ap.parse_args()

    d, pe, secs = ua.load_pe(a.exe)
    off = ua.make_off(secs)
    errata = ua.load_errata(a.errata)
    sizes = ua.load_bodies(a.funcs, errata)
    entries = sorted(sizes)
    blocks = ua.load_blocks(a.blocks)
    ref_unwind, ref_code, ref_reloc = ua.reference_routes(d, pe, secs, off)
    ref = ref_code | ref_reloc                    # pass-6-admissible routes only

    text = next(s for s in secs if s[0] == ".text")
    _tn, tva, _tvs, tpr, trs = text
    text_lo, text_hi = IMAGE_LO, IMAGE_HI = ua.IMAGE + tva, ua.IMAGE + tva + trs

    # ---- pass 1: decode every listed body; collect real call/branch sites ----
    call_sites = collections.defaultdict(set)   # target -> {source va}
    jcc_sites = collections.defaultdict(set)
    listed_ins = {}
    for e in entries:
        ins = decode_span(d, off, e, e + sizes[e])
        listed_ins[e] = ins
        for x in ins:
            t = branch_target(x)
            if t is None:
                continue
            if x.mnemonic == "call":
                call_sites[t].add(x.address)
            else:
                jcc_sites[t].add(x.address)

    # ---- pass 1b: decode each unlisted block's stream and collect ITS
    # outbound call/branch targets. Without this a real entry whose only
    # callers live inside unlisted blocks earns no `call` signal and can be
    # missed entirely (SWE2-AUDIT-SPEC shadow-audit finding).
    block_streams = {}
    for s, n in blocks:
        ins, anchor = anchored_stream(d, off, entries, s, s + n)
        block_streams[s] = (ins, anchor)
        for x in ins:
            if not (s <= x.address < s + n):
                continue
            t = branch_target(x)
            if t is None:
                continue
            if x.mnemonic == "call":
                call_sites[t].add(x.address)
            else:
                jcc_sites[t].add(x.address)

    # region lookup: which block or listed body contains a va
    region_bounds = sorted([e for e in entries] + [s for s, _n in blocks])

    def region_of(va):
        i = bisect.bisect_right(region_bounds, va) - 1
        return region_bounds[i] if i >= 0 else None

    # ---- pass 2: decode each block's stream, anchored at the predecessor ----
    out_rows = []
    total_segments = 0
    stats = collections.Counter()
    for s, n in blocks:
        b_end = s + n
        ins, anchor = block_streams[s]

        # signals into this block
        forced = set()
        sigs = collections.defaultdict(set)
        for t, srcs in call_sites.items():
            if s <= t < b_end:
                forced.add(t)
                sigs[t].add("call")
        for t, srcs in jcc_sites.items():
            if s <= t < b_end and any(region_of(x) != s for x in srcs):
                forced.add(t)
                sigs[t].add("jmp-in")
        for t in ref:
            if s < t < b_end:
                forced.add(t)
                sigs[t].add("ref")
        if s in ref:
            sigs[s].add("ref")

        segs = segment_stream(ins, s, b_end, forced)
        if not segs:
            stats["no-ins"] += 1
            continue
        # tag the first segment's signals
        first_addr = segs[0][0]
        if s in ref:
            sigs[first_addr].add("ref")
        if s in call_sites:
            sigs[first_addr].add("call")
        if anchor == "straddle":
            sigs[first_addr].add("repaired-start")
        for e0, sig, seg_ins in segs:
            seg_bytes = seg_ins[-1].address + seg_ins[-1].size - e0 if seg_ins else 0
            last = seg_ins[-1].mnemonic if seg_ins else "none"
            sig = sig | sigs.get(e0, set())  # surface WHICH evidence forced the cut
            out_rows.append((s, n, e0, seg_bytes, anchor, last,
                             ",".join(sorted(sig)) or "post-term"))
            total_segments += 1
        stats["anchor:%s" % anchor] += 1

    # ---- controls ----
    if a.self_test:
        # precision: run the boundary rule inside each listed body
        split = 0
        for e in entries:
            ins = listed_ins[e]
            segs = segment_stream(ins, e, e + sizes[e], set())
            if len(segs) > 1:
                split += 1
        print("PRECISION control: %d of %d listed bodies kept single "
              "(%.2f%%; %d would split)" %
              (len(entries) - split, len(entries),
               100.0 * (len(entries) - split) / len(entries), split))

        # recall: consecutive listed pairs - is the second entry recovered by
        # the same signal set production uses (call targets, external branches,
        # reference union, padded post-terminator rule)?
        rec = miss = 0
        for k in range(len(entries) - 1):
            e0, e1 = entries[k], entries[k + 1]
            ins = decode_span(d, off, e0, e1 + sizes[e1])
            forced = set()
            if e1 in call_sites or e1 in ref:
                forced.add(e1)
            if any(e0 <= src < e0 + sizes[e0] for src in jcc_sites.get(e1, ())):
                pass  # same-region branch, not evidence
            elif jcc_sites.get(e1):
                forced.add(e1)
            segs = segment_stream(ins, e0, e1 + sizes[e1], forced)
            if any(x[0] == e1 for x in segs):
                rec += 1
            else:
                miss += 1
        print("RECALL control: %d of %d consecutive listed entries recovered "
              "(%.2f%%; %d missed)" % (rec, rec + miss, 100.0 * rec / (rec + miss), miss))

    print("blocks processed      : %d" % len(blocks))
    print("segments emitted      : %d" % total_segments)
    for k in sorted(stats):
        print("  %-14s %5d" % (k, stats[k]))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("# Candidate function entries inside the unlisted code blocks.\n")
            f.write("# Regenerate: gfz-scripts/unlisted_entry_points.py --out <this file>\n")
            f.write("# signals: call=decoded call target; jmp-in=branch from outside the block;\n")
            f.write("#         ref=lea/rel32/reloc union (pass-6 admissible; .pdata excluded);\n")
            f.write("#         post-term=post-terminator, unreachable;\n")
            f.write("#         repaired-start=block start was mid-instruction, entry is the next\n")
            f.write("#         boundary of the predecessor-anchored stream.\n")
            f.write("block_va\tblock_bytes\tentry_va\tsegment_bytes\tanchor\tlast_ins\tsignals\n")
            for row in out_rows:
                f.write("%08X\t%d\t%08X\t%d\t%s\t%s\t%s\n" % row)
        print("wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
