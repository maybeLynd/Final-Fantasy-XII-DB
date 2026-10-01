"""SWE2-AUDIT-SPEC independent check of the RC-36 withdrawal statements and the RC-35 caller set (2026-09-30).
Reads the image only (tk.py) and the raw call index. Prints facts; judged in REVIEW.md."""
import sys, json, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
def callers(t): return sorted(int(x, 16) for x in RAW.get("%X" % t, []))
def body(e):
    return list(tk.fdis(e))
def show(tag, e):
    print("--", tag, "%08X" % e, "owner", tk.fname(e) if tk.owner(e) else None)

# 1. owner of 003C25BD and the instruction there; the call at 003C258B
for a in (0x3C25BD, 0x3C258B, 0x3BE554):
    o = tk.owner(a); oe = o[0] if isinstance(o, tuple) else o
    ins = [x for x in tk.dis(a, a + 16)][:1]
    print("site %08X owner=%s insn=%s" % (a, ("%08X" % oe) if oe else None, ins[0].mnemonic + " " + ins[0].op_str if ins else None))

# 2. does 003C2320 call 003BF430 or read [..+0xe0]; does 003BE3A0 call 003BF430
for e in (0x3C2320, 0x3BE3A0):
    ins = body(e)
    calls = [(x.address, x.op_str) for x in ins if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")]
    tgt = sorted(set(int(s, 16) for _, s in calls))
    e0 = [("%08X" % x.address, x.op_str) for x in ins if re.search(r"\+ 0xe0\]", x.op_str)]
    c0c = [("%08X" % x.address, x.mnemonic, x.op_str) for x in ins if re.search(r"\+ 0xc\]", x.op_str)]
    print("fn %08X ninsn=%d calls_3BF430=%s e0_operands=%s" % (e, len(ins), 0x3BF430 in tgt, e0))
    print("   +0x0C operands:", c0c[:12])
    print("   direct callees:", " ".join("%08X" % t for t in tgt))
# 3. raw callers
for t in (0x3C2320, 0x3BE3A0, 0x3BF430, 0x3BE680, 0x3BDDE0):
    cs = callers(t)
    print("raw callers of %08X: %d -> %s" % (t, len(cs), " ".join("%08X@%s" % (c, "%08X" % (tk.owner(c)[0] if isinstance(tk.owner(c), tuple) else (tk.owner(c) or 0))) for c in cs[:30])))
