"""sd5_thunks.py - SWE2-AUDIT-SPEC (2026-09-30). 0017F150 (`jmp [vt+0x60]`, slot 12) and 0017F250 (`jmp [vt+0x90]`,
slot 18) are generic virtual-call thunks. List every raw rel32 caller and the instruction that last sets rcx before the
call, and flag a caller whose rcx comes from the application holders 01F7E350 (static object) / 02EA5368 (pointer).
Also lists rip references to those two holders inside the callers' owners.
"""
import sys, struct
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk  # noqa: E402
TG = [0x0017F150, 0x0017F250]
HOLD = (0x01F7E350, 0x02EA5368)
text = tk.d[tk.TRO:tk.TRO + tk.TRS]
refs = {t: [] for t in TG}
for p in range(len(text) - 6):
    b = text[p]
    if b in (0xE8, 0xE9):
        L, rel = 5, struct.unpack_from("<i", text, p + 1)[0]
    elif b == 0x0F and 0x80 <= text[p + 1] <= 0x8F:
        L, rel = 6, struct.unpack_from("<i", text, p + 2)[0]
    else:
        continue
    a = tk.TVA + p; t = a + L + rel
    if t in refs:
        x = tk._decode_at(a)
        if x is not None and x.size == L:
            refs[t].append(a)
flag = 0
for t in TG:
    print("%08X: %d raw rel32 references" % (t, len(refs[t])))
    for a in sorted(refs[t]):
        o, how = tk.owner(a)
        if o is None:
            print("  %08X (unowned)" % a); continue
        n = tk.fsize(o) if how == "listed" else next(e - b for b, e in tk.pdata if b == o)
        xs = tk.dis(o, o + n)
        pre = [x for x in xs if x.address < a][-8:]
        rc = next(("%s %s" % (x.mnemonic, x.op_str) for x in reversed(pre) if x.op_str.startswith(("rcx", "ecx"))), "?")
        hold = []
        for x in xs:
            if "rip" in x.op_str:
                for op in x.operands:
                    if op.type == 3 and op.mem.base == 41:   # X86_REG_RIP
                        tgt = x.address + x.size + op.mem.disp
                        if tgt in HOLD: hold.append("%08X->%08X" % (x.address, tgt))
        if hold: flag += 1
        print("  %08X in %-60s rcx: %-40s app-holder refs in owner: %s" % (a, tk.fname(a), rc, " ".join(hold) or "-"))
print("callers whose owner touches an application holder: %d" % flag)
