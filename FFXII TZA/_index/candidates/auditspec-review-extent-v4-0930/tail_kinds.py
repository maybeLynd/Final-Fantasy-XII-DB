"""tail_kinds.py - SWE2-AUDIT-SPEC: classify each of the 254 extended tails (listed end -> chain end).
  pad      : only CC/90 bytes
  jtable   : after alignment to 4, a leading run of >= 2 dwords that are RVAs whose VA lies inside [root, chain end)
             (MSVC switch tables are image-relative dwords; a byte index table may follow the dword table)
  code     : the tail start is a branch target from inside [root, chain end) or the listed body falls through into it
  other    : none of the above
Also: for jtable rows, whether the table is actually referenced (an insn in the body forms its address: lea reg,[rip+..]
resolving into the tail or a [reg+reg*4+disp] with disp = table RVA)."""
import os, sys, struct, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "work", "FABLE", "takebacks"))
import tk
BASE = tk.BASE
txt = subprocess.run(["git", "-C", ROOT, "show", "d20226c17:Database/FFXII TZA/_index/FUNCTION-EXTENT-ERRATA.tsv"], capture_output=True).stdout.decode()
rows = []
for i, line in enumerate(txt.splitlines()):
    p = line.split("\t")
    if i and len(p) >= 15 and p[14].strip() == "pdata-chain":
        rows.append((int(p[0], 16), int(p[3], 16), int(p[12], 16)))
kinds, kbytes = collections.Counter(), collections.Counter()
examples = collections.defaultdict(list)
jt_ref = 0
for r, le, ce in rows:
    raw = tk.d[tk.off(le):tk.off(le) + (ce - le)]
    kind = None
    if set(raw) <= {0xCC, 0x90}:
        kind = "pad"
    else:
        a = le
        while a < ce and (a & 3):
            a += 1
        n = (ce - a) // 4
        if n >= 2:
            vals = [struct.unpack_from("<I", tk.d, tk.off(a) + 4 * k)[0] for k in range(n)]
            lead = 0
            while lead < n and r <= BASE + vals[lead] < ce:
                lead += 1
            if lead >= 2:
                kind = "jtable"
                ins = tk.dis(r, le)
                for x in ins:
                    for op in x.operands:
                        if op.type == 3:  # mem
                            if op.mem.index != 0 and a <= BASE + (op.mem.disp & 0xFFFFFFFF) < ce:
                                jt_ref += 1; break
                            if x.mnemonic == "lea" and x.reg_name(op.mem.base) == "rip" and a <= x.address + x.size + op.mem.disp < ce:
                                jt_ref += 1; break
                    else:
                        continue
                    break
    if kind is None:
        ins = tk.dis(r, ce)
        tg = {x.operands[0].imm for x in ins if x.mnemonic.startswith("j") and x.operands and x.operands[0].type == 2}
        last = [x for x in ins if x.address < le]
        ft = last and last[-1].address + last[-1].size == le and last[-1].mnemonic not in ("ret", "jmp", "int3")
        kind = "code" if (le in tg or ft or any(le <= t < ce for t in tg)) else "other"
    kinds[kind] += 1; kbytes[kind] += ce - le
    if len(examples[kind]) < 6:
        examples[kind].append("%08X(+%d)" % (r, ce - le))
print("tail kinds (rows):", dict(kinds))
print("tail kinds (bytes):", dict(kbytes), "total", sum(kbytes.values()))
print("jtable rows whose table address is formed in the listed body (image-base index form or rip lea): %d of %d" % (jt_ref, kinds["jtable"]))
for k, v in examples.items():
    print("  %-7s %s" % (k, " ".join(v)))
