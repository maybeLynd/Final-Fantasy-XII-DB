"""ticket_done.py - find code that advances a request ticket's done counter (word +0x18) and compares it
with the requested counter (word +0x1A), i.e. the pending-completion route that emits message 16 later.
Positive control: 00249410 (the submit-time compare `cmp word ptr [rcx + 0x1a], ax`) must be listed.
Run from pub140-scratch: python ../ovprobes/ticket_done.py"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(HERE, "..", "pub140-scratch"))
sys.argv = ['disw', '0031EB20']
exec(open('disw.py').read().split("fn = int")[0])
hits = {}
for fs, sz in sorted(funcs.items()):
    if not (0x121000 <= fs < 0x8C1635):
        continue
    code = d[off(fs):off(fs) + sz]
    has_cmp = has_18 = False
    lines = []
    for ins in md.disasm(code, fs):
        s = ins.op_str
        if re.search(r"word ptr \[r\w+ \+ 0x1a\]", s) and ins.mnemonic == "cmp":
            has_cmp = True; lines.append(f"{ins.address:08X} {ins.mnemonic} {s}")
        if re.search(r"word ptr \[r\w+ \+ 0x18\]", s) and ins.mnemonic in ("inc", "add", "mov", "cmp"):
            has_18 = True; lines.append(f"{ins.address:08X} {ins.mnemonic} {s}")
    if has_cmp:
        hits[fs] = (has_18, lines)
for fs, (h18, lines) in hits.items():
    print(f"== {fs:08X} {names.get(fs, '')} size {funcs[fs]:#x} touches+18={h18}")
    for l in lines[:8]:
        print("   ", l)
print("CONTROL 00249410 listed:", 0x249410 in hits)
