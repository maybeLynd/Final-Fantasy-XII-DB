"""tail_bytes.py - SWE2-AUDIT-SPEC: decode the extended tails of spot rows (listed end -> chain end) and the last listed
instructions; flag int3/nop-only tails, and count over all 254 rows how many tails are pure padding (CC/90) and how many are
reached by a branch from inside the listed body or the chain. Linear decode from each chain fragment start."""
import os, sys, struct, io, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "work", "FABLE", "takebacks"))
import tk
txt = subprocess.run(["git", "-C", ROOT, "show", "d20226c17:Database/FFXII TZA/_index/FUNCTION-EXTENT-ERRATA.tsv"], capture_output=True).stdout.decode()
rows = []
for i, line in enumerate(txt.splitlines()):
    p = line.split("\t")
    if i and len(p) >= 15 and p[14].strip() == "pdata-chain":
        rows.append((int(p[0], 16), int(p[3], 16), int(p[12], 16)))
SPOT = [0x002A8550, 0x003A1E50, 0x00462540, 0x007B2CB0, 0x0082D410]
def decode(a, b):
    return [x for x in tk.dis(a, b)]
pad, reached, ret_in_tail, total_bytes = 0, 0, 0, 0
kinds = collections.Counter()
for r, le, ce in rows:
    raw = tk.d[tk.off(le):tk.off(le) + (ce - le)]
    total_bytes += ce - le
    if set(raw) <= {0xCC, 0x90}:
        pad += 1; kinds["pad-only"] += 1
    ins = decode(r, ce)
    tail = [x for x in ins if x.address >= le]
    if any(x.mnemonic in ("ret", "jmp") for x in tail): ret_in_tail += 1
    # is the tail start reached by a branch from anywhere in [r, ce)?
    tgt = set()
    for x in ins:
        if x.mnemonic.startswith("j") and x.operands and x.operands[0].type == 2:
            tgt.add(x.operands[0].imm)
    if any(le <= t < ce for t in tgt): reached += 1
    # does the listed body end on an instruction boundary that falls through into the tail?
    last = [x for x in ins if x.address < le]
    lm = last[-1].mnemonic if last else "-"
    kinds["listed-last=" + ("ret/jmp" if lm in ("ret", "jmp", "int3") else "other")] += 1
print("rows %d, tail bytes %d, pad-only tails %d, tails holding ret/jmp %d, tails a branch target from the body %d" % (
    len(rows), total_bytes, pad, ret_in_tail, reached))
print("listed body's last instruction:", dict(kinds))
for r in SPOT:
    le, ce = next((b, c) for a, b, c in rows if a == r)
    ins = decode(r, ce)
    print("SPOT %08X listed_end %08X chain_end %08X (%s)" % (r, le, ce, tk.fname(r)))
    for x in [x for x in ins if x.address < le][-2:] + [x for x in ins if x.address >= le][:6]:
        print("   %s %08X %-6s %s" % (">" if x.address >= le else " ", x.address, x.mnemonic, x.op_str))
    refs = [x.address for x in ins if x.mnemonic.startswith("j") and x.operands and x.operands[0].type == 2 and le <= x.operands[0].imm < ce]
    print("   branches into tail from:", " ".join("%08X" % a for a in refs) or "none")
