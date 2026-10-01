"""The staged head-look command of a character render record: builders, forwarders, services, script verbs.

A character render record carries a 0x50-byte command record at +0x580. Eighteen record-level forwarders
(`add rcx, 0x580` / `jmp builder`) each stage one kind of change by setting a request bit (and sometimes a value bit
and a payload) in the record's flag dword; the dirty-state pass later hands the record to the applier 003E37F0 and
clears it. This script walks the chain outward from the forwarders:

  builder  <- forwarder  <- actor-service function (direct call)  <- verb handler (direct call or tail jump,
  or one further hop through a caller that is not itself a verb handler - printed as `via`)

and names each handler from scriptvm-verb-table.tsv (any column holding the handler's address).
Control: the forwarder list is rebuilt from the image by searching every listed function for `add rcx, 0x580`
followed by a `jmp`, and must have 18 members.
"""
import struct, sys, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
VERBS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\01-Script-VM-Native-Bridge\Verb-Dispatch\scriptvm-verb-table.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, ro, rs))
    o += 40


def off(va):
    rva = va - BASE
    for a, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


md = Cs(CS_ARCH_X86, CS_MODE_64)
funcs = {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        funcs[int(p[0], 16)] = (p[1], int(p[2]))
    except (ValueError, IndexError):
        pass
verb_of = collections.defaultdict(list)
for l in open(VERBS, encoding="utf-8", errors="replace"):
    p = l.rstrip("\n").split("\t")
    if len(p) < 5 or p[0] == "call_id":
        continue
    for c in p[5:]:
        if len(c) == 8:
            try:
                verb_of[int(c, 16)].append("%s (%s)" % (p[3], p[0]))
            except ValueError:
                pass

# one linear pass: direct call / jmp edges, and the forwarder pattern
edges = collections.defaultdict(set)      # target -> {caller function}
forwarders = {}
for fa, (name, size) in funcs.items():
    fo = off(fa)
    if fo is None or size <= 0:
        continue
    ins = list(md.disasm(d[fo:fo + size], fa))
    for k, x in enumerate(ins):
        if x.mnemonic in ("call", "jmp"):
            try:
                edges[int(x.op_str, 16)].add(fa)
            except ValueError:
                pass
    if len(ins) >= 2 and ins[0].mnemonic == "add" and ins[0].op_str == "rcx, 0x580" and ins[1].mnemonic == "jmp":
        try:
            forwarders[fa] = int(ins[1].op_str, 16)
        except ValueError:
            pass


def summary(builder):
    fo = off(builder)
    size = funcs.get(builder, ("", 64))[1]
    out = []
    for x in md.disasm(d[fo:fo + size], builder):
        if x.mnemonic in ("or", "and", "bts", "btr", "xor") or (x.mnemonic in ("mov", "movss") and "ptr [rcx" in x.op_str.split(", ")[0]):
            out.append("%s %s" % (x.mnemonic, x.op_str))
    return "; ".join(out)


print("# forwarders found %d (control: 18)" % len(forwarders))
print("forwarder\tbuilder\tbuilder_stores\tservice_callers\tverbs")
for f in sorted(forwarders):
    b = forwarders[f]
    services = sorted(edges.get(f, ()))
    verbs = set()
    for s in services:
        verbs.update(verb_of.get(s, ()))
        for h in edges.get(s, ()):
            verbs.update(verb_of.get(h, ()))
            if not verb_of.get(h):
                for h2 in edges.get(h, ()):          # one more hop, only through a caller that is not itself a verb
                    verbs.update(v + " via %08X" % h for v in verb_of.get(h2, ()))
    print("%08X\t%08X\t%s\t%s\t%s" % (f, b, summary(b), " ".join("%08X" % s for s in services), ", ".join(sorted(verbs)) or "-"))
