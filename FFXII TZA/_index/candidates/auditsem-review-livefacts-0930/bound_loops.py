"""SWE2-AUDIT-SEM: for each unknown-count inline loop below a target (filter_targets.out), print base, distance to the
target, and the loop's exit compare(s) with any immediate or rip-relative end address, so its extent can be bounded
by reading. Targets: T1 0215EFF4, T2 01E02804/01E02810."""
import re, csv
import img
rows = {r["head"]: r for r in csv.DictReader(open("inline_bulk.tsv"), delimiter="\t")}
want = []
for line in open("filter_targets.out"):
    if line.startswith("=="):
        tgt = int(line.split()[2], 16)
    m = re.search(r"UNKNOWN-COUNT below target: (\w+)", line)
    if m and (m.group(1), tgt) not in want:
        want.append((m.group(1), tgt))
def ript(x):
    m = re.search(r"rip ([+-]) (0x[0-9a-f]+)", x.op_str)
    return x.address + x.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1) if m else None
for head, tgt in want:
    r = rows[head]
    base = int(r["base_const"], 16)
    h, j = int(r["head"], 16), int(r["jump"], 16)
    body = [x for x in img.md.disasm(img.rd(h, j - h + 16), h) if x.address <= j]
    cmps = []
    for x in body:
        if x.mnemonic in ("cmp", "sub", "dec", "inc", "test"):
            t = ript(x)
            cmps.append("%08X %s %s%s" % (x.address, x.mnemonic, x.op_str, " [=%08X]" % t if t else ""))
    print("%s base %08X stride %s  target-base %#x (%s iterations to reach)  exits: %s" % (
        head, base, r["stride"], tgt - base, (tgt - base) // int(r["stride"], 16), " | ".join(cmps)))
