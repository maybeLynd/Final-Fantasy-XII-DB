# frontier_clones.py - group non-UC-1 frontier bodies by (a) exact bytes and (b) an operand-masked
# form: rel32 call/jmp targets and rip-relative displacements replaced, everything else kept. A group
# is a candidate shared body shape; it is not a family (no provenance, no controls yet).
import os, sys, io, csv, struct, collections, hashlib
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
sys.path.insert(0, ROOT + r"\Database\Tools\analysis-kit\gfz-scripts")
import check_dispositions as CD
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
WK = ROOT + r"\Database\Tools\work"
sizes = CD.load_functions()
d = open(WK + r"\exe\FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((0x120000 + va, vs, ro, rs))
def off(a):
    for va, vs, ro, rs in secs:
        if va <= a < va + rs:
            return ro + (a - va)
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
R = list(csv.DictReader(open(WK + r"\SWE2-EC7\frontier-partition-0929.tsv", encoding="utf-8"), delimiter="\t"))
def masked(e):
    b = bytearray(d[off(e):off(e) + sizes[e]])
    for x in md.disasm(bytes(b), e):
        k = x.address - e
        if x.mnemonic in ("call", "jmp") and x.size == 5 and b[k] in (0xE8, 0xE9):
            b[k + 1:k + 5] = b"\0\0\0\0"
        elif x.disp_offset and "rip" in x.op_str:
            b[k + x.disp_offset:k + x.disp_offset + x.disp_size] = b"\0" * x.disp_size
    return bytes(b)
exact, mask = collections.defaultdict(list), collections.defaultdict(list)
scope = [r for r in R if r["uc1"] != "Y"]
for r in scope:
    e = int(r["entry"], 16)
    raw = d[off(e):off(e) + sizes[e]]
    exact[hashlib.sha1(raw).hexdigest()].append(r)
    mask[hashlib.sha1(masked(e)).hexdigest()].append(r)
def report(g, label):
    big = sorted((v for v in g.values() if len(v) >= 4), key=len, reverse=True)
    print("%s: %d groups of >=4 holding %d bodies; groups of >=2 hold %d" % (
        label, len(big), sum(map(len, big)), sum(len(v) for v in g.values() if len(v) >= 2)))
    for v in big[:15]:
        print("   %4d x %4s B  shape=%-22s e.g. %s  owners=%s" % (len(v), v[0]["bytes"], v[0]["shape"], v[0]["entry"],
              dict(collections.Counter((x["owner"] or x["domain_head"] or "-") for x in v).most_common(3))))
    return big
report(exact, "exact bytes")
big = report(mask, "operand-masked")
with io.open(WK + r"\SWE2-EC7\frontier-clone-groups-0929.tsv", "w", encoding="utf-8", newline="\n") as f:
    f.write("group\tsize\tentry\tbytes\tshape\towner_or_domain\n")
    for gi, v in enumerate(big):
        for x in v:
            f.write("M%03d\t%d\t%s\t%s\t%s\t%s\n" % (gi, len(v), x["entry"], x["bytes"], x["shape"], x["owner"] or x["domain_head"]))
