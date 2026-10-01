"""SWE2-AUDIT-SPEC: FABLE's second marker +0x0C reader 003BEB06 - owner, form, and whether the OPUS census could see it;
and whether the census output names 003C25A4 (a read of 003BDDE0's returned point inside 003C2320). 2026-09-30."""
import sys, re, json
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
RAW = json.load(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\tools\rawcalls.json"))
a = 0x3BEB06
x = tk.dis(a, a + 16)[0]
o = tk.owner(a)[0]
print("site %08X insn: %s %s ; owner %s" % (a, x.mnemonic, x.op_str, tk.fname(a)))
ins = tk.fdis(o)
tg = set(int(i.op_str, 16) for i in ins if i.mnemonic == "call" and i.op_str.startswith("0x"))
print("owner calls 003BF430:", 0x3BF430 in tg, "; owner has a +0xe0 operand:", any(re.search(r"\+ 0xe0\]", i.op_str) for i in ins))
print("owner raw callers:", " ".join("%s@%08X" % (c, tk.owner(int(c, 16))[0]) for c in RAW.get("%X" % o, [])))
out = open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\lmap-rc35-rc36-0930\lmap_field_reads.out", encoding="utf-8").read()
for s in ("003C25A4", "003C25BD", "003BEB06", "003C2320", "003BE3A0", "003BDDE0"):
    print("census output mentions %s: %s" % (s, s in out.upper()))
