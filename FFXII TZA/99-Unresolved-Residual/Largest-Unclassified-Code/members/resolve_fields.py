"""resolve_fields.py FN [FN...]: for every call to ImageAddress_ResolveRuntimePointer (0020E600) in each function, the
instruction that loaded ecx before it (walking back within the same basic run, stopping at the previous call).
Histogram of the load forms, e.g. 'dword [rsi+0x170]' or 'dword [r14+rax*4+0x5a0]'. A call with no ecx load found is
reported as 'unresolved' - never guessed."""
import sys, struct, collections, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
RESOLVE = 0x0020E600
sizes = {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2])
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


md = Cs(CS_ARCH_X86, CS_MODE_64)
for fn in sys.argv[1:]:
    a = int(fn, 16)
    ins = list(md.disasm(d[v2o(a):v2o(a) + sizes[a]], a))
    hist = collections.Counter()
    total = 0
    for i, x in enumerate(ins):
        if x.mnemonic == "call" and x.op_str == hex(RESOLVE):
            total += 1
            form = "unresolved"
            for y in reversed(ins[max(0, i - 12):i]):
                if y.mnemonic == "call":
                    break
                if y.mnemonic in ("mov", "movzx", "lea") and (y.op_str.startswith("ecx,") or y.op_str.startswith("rcx,")):
                    form = re.sub(r"^[er]cx, ", "", y.op_str)
                    form = re.sub(r"\b(r\d+d?|e?[a-d]x|[er]?[sd]i|[er]bp|[er]sp)\b(?= \+|\])", "REG", form) if "--base-agnostic" in sys.argv else form
                    break
            hist[form] += 1
    print("== %s  resolves %d" % (fn, total))
    for f, c in hist.most_common(25):
        print("   %4d  %s" % (c, f))
