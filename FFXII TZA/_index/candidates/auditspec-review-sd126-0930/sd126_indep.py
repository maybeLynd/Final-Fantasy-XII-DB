"""sd126_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-126 (battle-HUD widget procedure arms).
Uses ../auditspec-review-sd141-0930/sdx.py (pefile + capstone, certified image; not retool.py or the package script).

  T  the two jump tables decoded from the bytes (002778C0: byte table 00279D98 -> dword table 00279D60, 45 ids;
     00405310: dword table 00405724, 19 ids), default arm = the most common target; the id sets compared with
     16-UI/Widget-Object-Model/widget-message-handlers.tsv.
  C  a recursive-descent reach per arm inside the function's .pdata chain extent (jcc both ways, direct jmp inside,
     MSVC jump tables resolved from the run of instructions before `jmp reg`, calls fall through, ret / int3 stop).
     An arm's OWN code = what it reaches minus what every other arm and the default reach. Its callees = the direct
     call targets in its own code (+ indirect calls and out-of-function jmps, listed). Compared with the package's
     README table, which lists the calls met by a straight-line walk from the arm start to the first jmp / ret.
  E  00808C40: first instructions (the cookie check the README calls "the common exit").
"""
import collections, csv, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-sd141-0930"))
import sdx  # noqa: E402
from capstone import CS_OP_IMM, CS_OP_REG, CS_OP_MEM  # noqa: E402

IB = sdx.IB
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def extent(f):
    rs = [(IB + e[0], IB + e[1]) for e in sdx.PD if sdx.root(IB + e[0]) == f]
    return min(a for a, b in rs), max(b for a, b in rs)


def resolve_table(run):
    """MSVC jump table from the instruction run ending in `jmp reg`: returns (targets, info) or (None, why)."""
    dt = bt = bound = None
    for i in run:
        for op in i.operands:
            if op.type == CS_OP_MEM and op.mem.base and i.reg_name(op.mem.base) != "rip" and op.mem.index:
                if op.mem.scale == 4 and i.mnemonic in ("mov", "movsxd"):
                    dt = IB + op.mem.disp
                elif op.mem.scale == 1 and i.mnemonic == "movzx":
                    bt = IB + op.mem.disp
        if i.mnemonic == "cmp" and len(i.operands) == 2 and i.operands[1].type == CS_OP_IMM:
            bound = i.operands[1].imm + 1
    if dt is None or bound is None:
        return None, "no table/bound (dt %s bound %s)" % (dt, bound)
    if bt is not None:
        idx = list(sdx.rd(bt, bound))
        n = max(idx) + 1
    else:
        idx = list(range(bound))
        n = bound
    tg = [struct.unpack("<I", sdx.rd(dt + 4 * k, 4))[0] + IB for k in range(n)]
    return [tg[k] for k in idx], "bt %s dt %08X bound %d" % ("%08X" % bt if bt else "-", dt, bound)


def reach(entry, lo, hi, tables_out):
    seen, calls, icalls, tails, unres = set(), [], [], [], []
    stack = [entry]
    while stack:
        a = stack.pop()
        run = []
        while lo <= a < hi and a not in seen:
            i = sdx.one(a)
            if i is None:
                break
            seen.add(a)
            run.append(i)
            nxt = a + i.size
            ops = i.operands
            if i.mnemonic == "call":
                if ops[0].type == CS_OP_IMM:
                    calls.append((a, ops[0].imm))
                else:
                    icalls.append((a, i.op_str))
                a = nxt
                continue
            if i.mnemonic in ("ret", "int3") or i.mnemonic.startswith("ud"):
                break
            if i.mnemonic == "jmp":
                if ops[0].type == CS_OP_IMM:
                    if lo <= ops[0].imm < hi:
                        stack.append(ops[0].imm)
                    else:
                        tails.append((a, ops[0].imm))
                elif ops[0].type == CS_OP_REG:
                    if a not in tables_out:
                        tables_out[a] = resolve_table(run[-12:])
                    tg, info = tables_out[a]
                    if tg:
                        stack.extend(tg)
                    else:
                        unres.append((a, info))
                else:
                    unres.append((a, "jmp " + i.op_str))
                break
            if i.group(7) and ops and ops[0].type == CS_OP_IMM:  # jcc
                if lo <= ops[0].imm < hi:
                    stack.append(ops[0].imm)
                else:
                    tails.append((a, ops[0].imm))
            a = nxt
    return seen, calls, icalls, tails, unres


hand = {r["handler"]: [int(x) for x in r["ids"].split(",")] for r in csv.DictReader(open(os.path.join(
    HERE, "..", "..", "..", "16-UI", "Widget-Object-Model", "widget-message-handlers.tsv"), encoding="utf-8"), delimiter="\t")
    if r["ids"]}

print("== T. jump tables")
t1, _ = resolve_table([sdx.one(0x002778FF), sdx.one(0x00277911), sdx.one(0x00277919)])
t2, _ = resolve_table([sdx.one(0x00405339), sdx.one(0x0040534B)])
print("  002778C0 prologue: %s | %s | %s | %s" % (sdx.txt(0x002778FF), sdx.txt(0x00277911), sdx.txt(0x00277919), sdx.txt(0x00277921)))
print("  00405310 prologue: %s | %s | %s" % (sdx.txt(0x00405339), sdx.txt(0x0040534B), sdx.txt(0x00405353)))
maps = {}
for f, tg in ((0x002778C0, t1), (0x00405310, t2)):
    cnt = collections.Counter(tg)
    dflt = cnt.most_common(1)[0][0]
    arms = {k + 1: t for k, t in enumerate(tg) if t != dflt}
    maps[f] = (arms, dflt)
    print("  %08X: %d ids, default %08X x%d; arms %s" % (f, len(tg), dflt, cnt[dflt],
                                                        ", ".join("%d->%08X" % kv for kv in sorted(arms.items()))))
    check("T-%08X" % f, sorted(arms) == hand["%08X" % f], "id set equals widget-message-handlers.tsv %s" % hand["%08X" % f])
# compare chains (package A3/A4 read by the parked worker and re-checked here from the bytes)
maps[0x003FDFE0] = ({1: 0x003FE2EC, 10: 0x003FE2DF, 12: 0x003FE07E, 15: 0x003FE377, 18: 0x003FE035}, 0x003FE02B)
maps[0x003FF360] = ({1: 0x003FF59D, 8: 0x003FF560, 10: 0x003FF3B1, 12: 0x003FF6EA, 18: 0x003FF8DD, 19: 0x003FF892,
                     285: 0x003FF7AB}, 0x003FF79E)
for a in (0x003FE000, 0x003FE003, 0x003FE006, 0x003FE00C, 0x003FE00F, 0x003FE015, 0x003FE018, 0x003FE01A, 0x003FE01D,
          0x003FE023, 0x003FE026, 0x003FE028, 0x003FE02B):
    print("  003FDFE0 %08X %s" % (a, sdx.txt(a)))
for a in (0x003FF384, 0x003FF387, 0x003FF38A, 0x003FF390, 0x003FF396, 0x003FF399, 0x003FF39F, 0x003FF3A2, 0x003FF3A8,
          0x003FF3AB, 0x003FF784, 0x003FF787, 0x003FF78D, 0x003FF790, 0x003FF796, 0x003FF79C, 0x003FF79E, 0x003FF7A1):
    print("  003FF360 %08X %s" % (a, sdx.txt(a)))

README = {  # the package README's "direct callees" column, per (procedure, arm)
    (0x002778C0, 0x00277925): {0x00274BA0, 0x00245000, 0x00244960, 0x00247950, 0x002470D0},
    (0x002778C0, 0x00278A3B): {0x00274BD0}, (0x002778C0, 0x00278074): {0x00275440, 0x0027CD00},
    (0x002778C0, 0x00277A64): {0x00249C60, 0x00244F00}, (0x002778C0, 0x00278302): set(),
    (0x002778C0, 0x00279CC5): {0x00368A50}, (0x002778C0, 0x00279CF9): {0x00290B70, 0x00245020, 0x002470C0},
    (0x002778C0, 0x0027902D): {0x002753F0, 0x00247260}, (0x002778C0, 0x00279187): {0x002D47C0, 0x00275440},
    (0x002778C0, 0x00278FCA): set(), (0x002778C0, 0x002780E8): {0x0027C280, 0x0028F800, 0x00296AF0, 0x00275440},
    (0x002778C0, 0x00279C7E): set(), (0x002778C0, 0x00279CA5): set(),
    (0x00405310, 0x00405358): {0x003946B0, 0x00394690, 0x00394720, 0x00244F50, 0x00405770, 0x004060B0},
    (0x00405310, 0x004055BE): set(), (0x00405310, 0x0040564E): {0x00405C20}, (0x00405310, 0x00405500): {0x00405100},
    (0x00405310, 0x004056B0): {0x00244F00}, (0x00405310, 0x00405573): {0x004060B0},
    (0x003FDFE0, 0x003FE2EC): {0x003FD6B0}, (0x003FDFE0, 0x003FE2DF): {0x003FDAD0},
    (0x003FDFE0, 0x003FE07E): {0x002527B0, 0x0035D330, 0x002CCA10, 0x002CCA00}, (0x003FDFE0, 0x003FE377): set(),
    (0x003FDFE0, 0x003FE035): {0x003697F0},
    (0x003FF360, 0x003FF59D): {0x002432B0, 0x00247570, 0x0029FB50, 0x002D48C0, 0x002CD4D0, 0x002CD3C0},  # "..."
    (0x003FF360, 0x003FF560): {0x002D45C0, 0x002445C0, 0x002D1AC0},
    (0x003FF360, 0x003FF3B1): {0x002D45C0, 0x002445C0, 0x00368240, 0x00282DF0, 0x002C1A80},
    (0x003FF360, 0x003FF6EA): {0x003FE6E0, 0x00291D70, 0x00293110, 0x002445C0, 0x002C22F0, 0x002470C0},
    (0x003FF360, 0x003FF8DD): set(), (0x003FF360, 0x003FF892): {0x0035D330, 0x002CCA10, 0x002CE2F0},
    (0x003FF360, 0x003FF7AB): {0x002D4650, 0x00247510},
}

print("== C. per-arm own code and callees")
tabs = {}
diff_rows = []
for f, (arms, dflt) in maps.items():
    lo, hi = extent(f)
    entries = sorted(set(arms.values()) | {dflt})
    R = {e: reach(e, lo, hi, tabs) for e in entries}
    fullr = reach(f, lo, hi, tabs)
    print("  %08X extent %08X..%08X; from entry: %d instructions, unresolved indirect jmps %s" % (
        f, lo, hi, len(fullr[0]), ["%08X (%s)" % u for u in fullr[4]]))
    for e in entries:
        others = set().union(*[R[x][0] for x in entries if x != e])
        own = R[e][0] - others
        oc = sorted({t for a, t in R[e][1] if a in own})
        oic = [(a, s) for a, s in R[e][2] if a in own]
        otl = sorted({t for a, t in R[e][3] if a in own})
        ids = [k for k, v in arms.items() if v == e]
        tag = "default" if e == dflt else "ids %s" % ids
        rd = README.get((f, e))
        extra = sorted(set(oc) - (rd or set())) if rd is not None else None
        missing = sorted((rd or set()) - set(oc)) if rd is not None else None
        print("    %08X %-14s own %4d ins; callees %s%s%s%s" % (
            e, tag, len(own), " ".join("%08X" % t for t in oc) or "none",
            "; indirect " + ", ".join("%08X %s" % x for x in oic) if oic else "",
            "; out-jmps " + " ".join("%08X" % t for t in otl) if otl else "",
            "" if rd is None else ("  | README %s; not in README: %s; README-only: %s" % (
                " ".join("%08X" % t for t in sorted(rd)) or "none", " ".join("%08X" % t for t in extra) or "-",
                " ".join("%08X" % t for t in missing) or "-"))))
        if rd is not None and (extra or missing):
            diff_rows.append((f, e, ids, extra, missing))
    for a, (tg, info) in sorted(tabs.items()):
        if lo <= a < hi:
            print("    table at jmp %08X: %s -> %s" % (a, info, "%d targets" % len(set(tg)) if tg else "UNRESOLVED"))
print("  arms whose own-code callees differ from the README column: %d" % len(diff_rows))

print("== E. 00808C40")
for i in sdx.md.disasm(sdx.rd(0x00808C40, 0x21), 0x00808C40):
    print("  %08X %s %s" % (i.address, i.mnemonic, i.op_str))
print("  raw callers of 00808C40 (E8/E9): %d" % len(sdx.rel32(0x00808C40)))
print("FAILS %d" % fails)
