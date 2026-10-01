"""getter_consumers.py GETTER: for each direct call to a singleton getter, the function the returned object is passed to.
Follows rax after the call through `mov rcx, rax` (or `mov rbx, rax` then `mov rcx, rbx`) to the next direct call or tail
jump within 8 instructions; reports that callee as the consumer. Sites where rax is only tested are counted as null checks.
Prints consumers grouped with their site counts."""
import sys, struct, collections, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
GET = int(sys.argv[1], 16)
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError):
        pass
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))


def v2o(v):
    for n, vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


raw = json.load(open("tools/rawcalls.json"))
sites = [int(s, 16) for s in raw.get("%X" % GET, [])]
md = Cs(CS_ARCH_X86, CS_MODE_64)
cons = collections.defaultdict(list)
nullchk = 0
for s in sites:
    o = v2o(s)
    ins = list(md.disasm(d[o:o + 64], s))[1:9]
    holders = {"rax"}
    got = None
    for y in ins:
        ops = y.op_str.replace(" ", "").split(",")
        if y.mnemonic == "mov" and len(ops) == 2 and ops[1] in holders:
            holders.add(ops[0])
            continue
        if y.mnemonic in ("call", "jmp") and y.op_str.startswith("0x"):
            if "rcx" in holders:
                got = int(y.op_str, 16)
            break
        if y.mnemonic == "test" and ops[0] in holders:
            continue
    if got is None:
        nullchk += 1
    else:
        cons[got].append(s)
print("getter %08X: %d call sites, %d passed on, %d not passed (null checks / field reads)" % (GET, len(sites), sum(len(v) for v in cons.values()), nullchk))
for c, ss in sorted(cons.items(), key=lambda kv: -len(kv[1])):
    print("  %08X %-45s %2d  %s" % (c, names.get(c, "")[:45], len(ss), " ".join("%08X" % x for x in ss[:5])))
