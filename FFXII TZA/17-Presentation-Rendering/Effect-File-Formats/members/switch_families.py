"""switch_families.py: every function with an MSVC x64 RVA jump table whose arms lead (by jmp/call within the first bytes of
the arm) to distinct handler functions; ranked by frontier handlers. Groups dispatchers that switch on the same
operand text (e.g. `byte ptr [rcx + 0x44]`) so method families over one type space show together.
Writes switch_families.tsv: dispatcher, name, cases, arm_targets, handler_functions, frontier_handlers, selector."""
import sys, re, struct, bisect, collections
sys.argv = ["x"]
exec(open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "jumptables.py")).read().split('if __name__ == "__main__":')[0])
front = set(int(l.split()[0], 16) for f in ("arch_frontier.txt", "c_frontier.txt") for l in open(f) if l.strip())
ks = sorted(sizes)
def own(s):
    i = bisect.bisect_right(ks, s) - 1
    return ks[i] if i >= 0 and ks[i] <= s < ks[i] + sizes[ks[i]] else None
def arm_handler(a, host):
    o = off(a)
    if o is None: return None
    for x in md.disasm(d[o:o + 40], a):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            t = int(x.op_str, 16)
            if own(t) != host and t in sizes: return t
        if x.mnemonic in ("ret", "jmp"): return None
    return None
def selector(f, site):
    o = off(f)
    ins = [x for x in md.disasm(d[o:o + sizes[f]], f) if x.address <= site]
    for x in reversed(ins[-14:]):
        if x.mnemonic in ("movzx", "mov", "movsx") and "ptr [" in x.op_str and ("byte" in x.op_str or "word" in x.op_str or "dword" in x.op_str):
            if "rip" not in x.op_str and "*4" not in x.op_str and "+ r" not in x.op_str.split("[")[1].split("]")[0].replace("+ 0x", ""):
                return re.sub(r"^\w+, ", "", x.op_str)
    return "-"
rows = []
for f in ks:
    if sizes[f] < 24: continue
    try: res = decode(f)
    except Exception: continue
    for site, tab, n, cases in res:
        hs = set()
        for t in cases:
            h = arm_handler(t, f)
            if h: hs.add(h)
        if len(hs) >= 8:
            rows.append((f, names.get(f, ""), n, len(cases), len(hs), len(hs & front), selector(f, site)))
rows.sort(key=lambda r: -r[5])
with open("switch_families.tsv", "w", encoding="utf-8", newline="\n") as fo:
    fo.write("dispatcher\tname\tcases\tarm_targets\thandler_functions\tfrontier_handlers\tselector\n")
    for r in rows: fo.write("%08X\t%s\t%d\t%d\t%d\t%d\t%s\n" % r)
print("dispatchers with >= 8 handler functions:", len(rows), "frontier handlers (with overlap):", sum(r[5] for r in rows))
for r in rows[:40]: print("%08X %-40s cases %3d arms %3d handlers %3d frontier %3d  %s" % r)
