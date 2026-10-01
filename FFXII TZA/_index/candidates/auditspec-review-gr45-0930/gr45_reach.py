"""gr45_reach.py - SWE2-AUDIT-SPEC review of rowflow.py's reach (GR-4/GR-5, 2026-09-30).

Uses the package's rowflow.py as the instrument UNDER TEST (read-only import; nothing written into the package) and the
independent loader img45.py for byte reads.

A1  what each propagation route contributes, over all 60 row offsets at depth 3: hits found with calls not followed
    (depth 0), with returns not followed, with outgoing stack arguments stripped. A route whose removal changes no hit
    has no positive control in this image.
A2  the hop-census positive control: how many of its 232 sites are found at depth 0 (inside the slot-referencing bodies,
    i.e. with no call hop at all).
A3  unmodelled uses: every walked instruction that READS a register carrying a row / base tag (rowflow's own probe) and
    is not one of the forms rowflow models (mov/movsxd/cmov reg,reg; lea; add; a memory base/index; a direct call's
    argument; a store; cmp/test). Listed by mnemonic with sites; the pointer-carrying kinds (push, movq/movd to xmm,
    xchg/cmpxchg, stores to a stack slot whose address is taken, and prologue home-slot spills) are examined.
A4  tagged stores into stack slots, and every `lea r, [rsp/rbp + d]` in the same function that could hand that slot's
    address to a callee (a pointer to a stack struct holding the row pointer).
"""
import os, sys, re, collections, threading

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "gr4-gr5-action-row-readers-0930")
sys.path.insert(0, PKG)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.setrecursionlimit(100000)


def main():
    import rowflow as RF
    R, SZ = RF.R, RF.SZ
    fns = RF.slot_functions()
    ALL = list(range(60))

    def hits(Fl):
        return {(h[1], h[4]) for h in Fl.hits}

    base = RF.Flow(ALL, 3)
    base.run(fns)
    H3 = hits(base)
    d0 = RF.Flow(ALL, 0)
    d0.run(fns)
    H0 = hits(d0)
    nr = RF.Flow(ALL, 3, follow_returns=False)
    nr.run(fns)
    HNR = hits(nr)

    class NoStack(RF.Flow):
        def step(self, f, x, st, depth):
            if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == 2:
                for k in [k for k in st if isinstance(k, tuple) and k[0] == "rsp" and 0x20 <= k[1] < 0x80]:
                    st.pop(k)
            return RF.Flow.step(self, f, x, st, depth)
    ns = NoStack(ALL, 3)
    ns.run(fns)
    HNS = hits(ns)
    print("A1 hits over 60 offsets, depth 3: %d (walked %d fns); depth 0: %d; returns off: %d; stack args stripped: %d"
          % (len(H3), len(base.entry), len(H0), len(HNR), len(HNS)))
    print("   needing a call hop: %d; lost without returns: %d %s; lost without stack args: %d %s"
          % (len(H3 - H0), len(H3 - HNR), sorted("%08X+%02X" % h for h in H3 - HNR)[:12],
             len(H3 - HNS), sorted("%08X+%02X" % h for h in H3 - HNS)[:12]))
    print("   rowflow's own counts: forms %d, handoffs %d, stackargs %d, row-returning fns %s"
          % (len(base.forms), len(base.handoffs), len(base.stackargs), sorted("%08X" % f for f in base.retsum)))
    for s in sorted(base.stackargs):
        print("   stackarg %08X@%08X -> %08X %s" % s)
    fh = collections.Counter(RF.cfg and next((f for f in base.entry if f <= a < f + SZ.get(f, 0)), None) for a, o in H3 - H0)
    print("   call-hop hits by function: %s" % {"%08X" % k: v for k, v in sorted(fh.items(), key=lambda kv: -kv[1])[:20]})

    # A2 hop census sites at depth 0
    tsv = os.path.join(PKG, "..", "..", "..", "07-Combat-Action", "Action-Definition-Row", "members", "action-row-reader-hops.tsv")
    rows = [l.rstrip("\r\n").split("\t") for l in open(tsv, encoding="utf-8")][1:]
    g0 = {a for a, o in H0}
    s0 = sum(1 for r in rows if int(r[4], 16) in g0)
    print("A2 hop-census sites %d; found at depth 0 (no call followed): %d; need a call hop: %d %s"
          % (len(rows), s0, len(rows) - s0, [r[4] for r in rows if int(r[4], 16) not in g0][:20]))

    # A3 unmodelled uses of a tagged register
    rowtag = lambda v: {t for t in v if t not in ("H", "F")}
    uses = collections.defaultdict(list)
    homespill = []
    for f in sorted(base.entry):
        blocks, succ, ind, end = RF.cfg(f)
        for b in blocks.values():
            for x in b:
                pr = base.probe.get(x.address)
                if not pr:
                    continue
                tagged = {r for r, v in pr.items() if rowtag(v)}
                if not tagged:
                    continue
                try:
                    rd_ = {RF.FAM.get(x.reg_name(r), x.reg_name(r)) for r in x.regs_access()[0]}
                except Exception:
                    rd_ = set()
                # registers used only as a memory base/index are modelled accesses
                memregs = set()
                for op in x.operands:
                    if op.type == 3:
                        memregs |= {RF.rn(x, op.mem.base), RF.rn(x, op.mem.index)}
                valregs = set()
                for op in x.operands:
                    if op.type == 1:
                        valregs.add(RF.rn(x, op.reg))
                live = (rd_ & tagged) - (memregs - valregs)
                if x.mnemonic in ("call",) or x.mnemonic.startswith("j"):
                    continue
                if not live:
                    continue
                m = x.mnemonic
                txt = "%s %s" % (m, x.op_str)
                ops = x.operands
                modelled = False
                if m in ("mov", "movsxd") or m.startswith("cmov"):
                    modelled = True     # reg copy or store (escape / stack slot)
                elif m in ("lea", "add") :
                    modelled = True
                elif m in ("cmp", "test"):
                    modelled = True
                if not modelled:
                    uses[m].append((f, x.address, txt, sorted(live)))
    print("A3 unmodelled instruction kinds reading a row/base-tagged register:")
    for m, L in sorted(uses.items(), key=lambda kv: -len(kv[1])):
        print("   %-10s %4d  e.g. %s" % (m, len(L), "; ".join("%08X %s" % (a, t) for f, a, t, r in L[:4])))
    carry = [u for m, L in uses.items() for u in L if m in ("push", "movq", "movd", "xchg", "cmpxchg", "movups", "movaps",
                                                            "movdqu", "movdqa", "pinsrq", "punpcklqdq", "stosq", "movnti")]
    print("A3 pointer-carrying unmodelled uses: %d" % len(carry))
    for f, a, t, r in carry:
        print("   %08X %08X %s %s" % (f, a, t, r))

    # A4 tagged stack stores, and address-taken stack in the same function
    stk = collections.defaultdict(set)
    for f in sorted(base.entry):
        blocks, succ, ind, end = RF.cfg(f)
        for b in blocks.values():
            for x in b:
                ops = x.operands
                if x.mnemonic == "mov" and len(ops) == 2 and ops[0].type == 3 and ops[1].type == 1 and ops[0].size >= 4:
                    br = RF.rn(x, ops[0].mem.base)
                    s = RF.rn(x, ops[1].reg)
                    if br in ("rsp", "rbp") and rowtag(base.probe.get(x.address, {}).get(s, set())):
                        stk[f].add((x.address, br, ops[0].mem.disp, "%s %s" % (x.mnemonic, x.op_str)))
    print("A4 functions with a row/base pointer stored to a stack slot: %d; stores %d" % (len(stk), sum(len(v) for v in stk.values())))
    for f, S in sorted(stk.items()):
        blocks, succ, ind, end = RF.cfg(f)
        leas = []
        prolog_sub = None
        for b in blocks.values():
            for x in b:
                if x.mnemonic == "lea" and x.operands[1].type == 3 and RF.rn(x, x.operands[1].mem.base) in ("rsp", "rbp") \
                        and not x.operands[1].mem.index:
                    leas.append((x.address, RF.rn(x, x.operands[1].mem.base), x.operands[1].mem.disp,
                                 "%s %s" % (x.mnemonic, x.op_str)))
        for a, br, d, t in sorted(S):
            near = [l for l in leas if l[1] == br and l[2] <= d < l[2] + 0x40 and not (l[3].startswith("lea rbp") or l[3].startswith("lea rsp"))]
            print("   %08X %08X %s%s" % (f, a, t, ("  | address-taken candidates: " + "; ".join("%08X %s" % (l[0], l[3]) for l in near)) if near else ""))
    # prologue home-slot spills of a tagged entry argument (before the frame is set up)
    for f in sorted(base.entry):
        dp, ent = base.entry[f]
        targs = {r for r, v in ent.items() if not isinstance(r, tuple) and rowtag(v)}
        if not targs:
            continue
        try:
            ins = list(R.md.disasm(R.at(f, min(SZ.get(f, 64), 48)), f))
        except Exception:
            continue
        for x in ins:
            if x.mnemonic == "sub" and x.op_str.startswith("rsp") or x.mnemonic == "push":
                break
            if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[0].type == 3 and x.operands[1].type == 1 \
                    and RF.rn(x, x.operands[0].mem.base) == "rsp" and RF.rn(x, x.operands[1].reg) in targs:
                homespill.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str)))
    print("A4 prologue home-slot spills of a tagged argument before the frame is set up: %d %s"
          % (len(homespill), ["%08X %08X %s" % h for h in homespill]))


th = threading.Thread(target=main)
threading.stack_size(256 * 1024 * 1024 - 4096)
th = threading.Thread(target=main)
th.start()
th.join()
