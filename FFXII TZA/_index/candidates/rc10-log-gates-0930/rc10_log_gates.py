"""rc10_log_gates.py - RC-10 (OPUS, 2026-09-30): does any caller of the formatted log call 005CDAA0 condition the call on a
global or per-thread value?  For every rel32 call to 005CDAA0 (raw E8 index over .text), the owning function is decoded
linearly, and every conditional jump in the function whose taken or fall-through path SKIPS the call site (a jcc before the
call whose target lies after it, within the function) is classified by what its flags come from: the compare/test that
last set flags before it and, one step back, the register load feeding that compare. A source counts as GLOBAL when it is
a rip-relative memory operand (or a register loaded from one), TLS when it uses gs:, else LOCAL. Output rc10_log_gates.tsv
and a summary of the globals that gate more than one site (a verbosity control would be shared)."""
import bisect, collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("%08X" % va)


fs = []
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            fs.append((int(p[0], 16), int(p[2])))
        except ValueError:
            pass
fs.sort(); starts = [a for a, _ in fs]


def owner(va):
    j = bisect.bisect_right(starts, va) - 1
    return fs[j] if j >= 0 and va < fs[j][0] + fs[j][1] else (None, None)


tx = [s for s in SECS if s[0] == ".text"][0]
T0, TR, TN = tx[1], tx[3], tx[4]
TARGET = 0x005CDAA0
sites = [T0 + m.start() for m in re.finditer(rb"[\xe8\xe9]", blob[TR:TR + TN - 4])
         if T0 + m.start() + 5 + struct.unpack("<i", blob[TR + m.start() + 1:TR + m.start() + 5])[0] == TARGET]
rip_target = lambda x: (x.address + x.size + int(re.search(r"rip ([+-]) 0x([0-9a-f]+)", x.op_str).group(2), 16)
                        * (1 if "rip +" in x.op_str else -1)) if "rip" in x.op_str else None
rows, gates = [], collections.defaultdict(list)
for site in sites:
    fa, fsz = owner(site)
    if fa is None:
        rows.append(("%08X" % site, "", "UNOWNED", "", "")); continue
    ins = list(md.disasm(blob[OFF(fa):OFF(fa) + fsz], fa))
    idx = {x.address: k for k, x in enumerate(ins)}
    if site not in idx:
        rows.append(("%08X" % site, "%08X" % fa, "DESYNC", "", "")); continue
    found = []
    for k, x in enumerate(ins):
        if x.address >= site:
            break
        if x.mnemonic.startswith("j") and x.mnemonic != "jmp" and x.operands and x.operands[0].type == X86_OP_IMM:
            t = x.operands[0].imm
            if not (site < t < fa + fsz):
                continue                                  # only branches that can jump over the call site
            flag = next((ins[j] for j in range(k - 1, max(-1, k - 8), -1) if ins[j].mnemonic in ("cmp", "test", "bt", "and", "or", "sub")), None)
            src, where = "LOCAL", ""
            if flag is not None:
                if "gs:" in flag.op_str:
                    src, where = "TLS", flag.op_str
                elif rip_target(flag):
                    src, where = "GLOBAL", "%08X" % rip_target(flag)
                else:
                    regs = [r.strip() for r in flag.op_str.split(",")]
                    for j in range(idx[flag.address] - 1, max(-1, idx[flag.address] - 10), -1):
                        y = ins[j]
                        d = y.op_str.split(",")[0].strip() if y.op_str else ""
                        if d and any(d[-2:] == r[-2:] for r in regs if r and not r.startswith(("0x", "byte", "dword", "qword", "word"))):
                            if "gs:" in y.op_str:
                                src, where = "TLS", y.op_str
                            elif rip_target(y) and y.mnemonic.startswith("mov"):
                                src, where = "GLOBAL", "%08X" % rip_target(y)
                            break
            found.append((x.address, src, where, "%s %s | %s" % (x.mnemonic, x.op_str, ("%s %s" % (flag.mnemonic, flag.op_str)) if flag else "?")))
    g = [f for f in found if f[1] in ("GLOBAL", "TLS")]
    for f in g:
        gates[f[2]].append(site)
    rows.append(("%08X" % site, "%08X" % fa, "GATED-GLOBAL" if g else ("GATED-LOCAL" if found else "UNGATED"),
                 ";".join("%08X %s %s" % (f[0], f[1], f[2]) for f in found)[:300], ";".join(f[3] for f in g)[:300]))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rc10_log_gates.tsv")
with io.open(out, "w", encoding="utf-8", newline="\n") as fo:
    fo.write("site\tfunction\tclass\tskipping_branches\tglobal_detail\n")
    for r in rows:
        fo.write("\t".join(r) + "\n")
c = collections.Counter(r[2] for r in rows)
print("sites %d in %d functions: %s" % (len(rows), len({r[1] for r in rows}), dict(c)))
fn_of = {int(r[0], 16): r[1] for r in rows}
multi = {k: sorted({fn_of[x] for x in v}) for k, v in gates.items()}
print("globals gating a log call: %d; gating sites in MORE than one function: %d" % (len(multi), sum(1 for v in multi.values() if len(v) > 1)))
for k, v in sorted(multi.items(), key=lambda kv: -len(kv[1])):
    print("  gate %-10s functions %s sites %d" % (k, " ".join(v), len(gates[k])))
