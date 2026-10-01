# BH-3: the two builder hubs 0037DF90 / 0037E0F0 - per-hub object and builder address ranges, and whether any builder
# touches data other than its own object (which would make call order matter).
import re
exec(open(r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\disw.py").read().split("fn = int")[0])
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
md.detail = True


def pairs(hub):
    ins = list(md.disasm(d[off(hub):off(hub) + funcs[hub]], hub))
    out, obj = [], None
    for x in ins:
        if x.mnemonic == "lea" and "rcx, [rip" in x.op_str:
            obj = x.address + x.size + int(re.search(r"0x[0-9a-f]+", x.op_str.split("+")[1]).group(0), 16)
        elif x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            out.append((obj, int(x.op_str, 16)))
            obj = None
    return out


H = {0x37DF90: pairs(0x37DF90), 0x37E0F0: pairs(0x37E0F0)}
for h, ps in H.items():
    objs = sorted(o for o, _ in ps if o)
    bs = sorted(b for _, b in ps)
    print("hub %08X: %d calls, objects %08X-%08X, builders %08X-%08X" % (h, len(ps), objs[0], objs[-1], bs[0], bs[-1]))
allobj = sorted((o, h) for h, ps in H.items() for o, _ in ps if o)
runs = []
for o, h in allobj:
    if not runs or runs[-1][0] != h:
        runs.append([h, 0])
    runs[-1][1] += 1
print("object-address order, runs by hub:", [("%X" % h, n) for h, n in runs])
allb = sorted((b, h) for h, ps in H.items() for _, b in ps)
runs = []
for b, h in allb:
    if not runs or runs[-1][0] != h:
        runs.append([h, 0])
    runs[-1][1] += 1
print("builder-address order, runs by hub:", [("%X" % h, n) for h, n in runs])

# foreign data touched by each builder: rip-relative operands outside the builder's own object neighbourhood
objset = {o for h, ps in H.items() for o, _ in ps if o}
foreign = 0
for h, ps in H.items():
    for obj, b in ps:
        if b not in funcs:
            print("  builder %08X not listed" % b)
            continue
        refs = set()
        calls = set()
        for x in md.disasm(d[off(b):off(b) + funcs[b]], b):
            if x.mnemonic == "call":
                calls.add(x.op_str)
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                    refs.add(x.address + x.size + op.mem.disp)
        other_objs = sorted(r for r in refs if r in objset and r != obj)
        data_refs = sorted(r for r in refs if 0x1DF0000 <= r < 0x3100000)
        if other_objs or data_refs or calls:
            foreign += 1
            print("  %08X (obj %08X): other objects %s, .data/.bss refs %s, calls %s" % (
                b, obj or 0, ["%08X" % r for r in other_objs][:4], ["%08X" % r for r in data_refs][:4], sorted(calls)[:4]))
print("builders with any rip-relative data reference or call:", foreign)
