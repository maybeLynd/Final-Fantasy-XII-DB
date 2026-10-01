"""rc1_records.py - RC-1's second half, static (OPUS, 2026-09-30): which class each caller of the query-record dispatcher
0031C5D0 writes into the record's dword +0 before the call. For each rel32 call site the owning function is decoded
linearly up to the call; RCX's last definition is found (lea rcx, [rsp + X] / mov rcx, reg), and for a stack record
the last store to dword [rsp + X] before the call is reported (an immediate, or the register it came from with that
register's last constant if any). Anything else is DYNAMIC with the instruction shown. Output rc1_records.tsv."""
import bisect, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64)


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
import sys
TARGET = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x0031C5D0
sites = [T0 + m.start() for m in re.finditer(rb"[\xe8\xe9]", blob[TR:TR + TN - 4])
         if T0 + m.start() + 5 + struct.unpack("<i", blob[TR + m.start() + 1:TR + m.start() + 5])[0] == TARGET]
rows = []
for site in sites:
    fa, fsz = owner(site)
    ins = [x for x in md.disasm(blob[OFF(fa):OFF(site) + 5], fa) if x.address <= site]
    if not ins or ins[-1].address != site:
        rows.append(("%08X" % site, "%08X" % (fa or 0), "DESYNC", "", "")); continue
    rcx_def = next((x for x in reversed(ins[:-1]) if x.op_str.split(",")[0].strip() in ("rcx", "ecx")), None)
    rd = "%s %s" % (rcx_def.mnemonic, rcx_def.op_str) if rcx_def else "entry rcx"
    m = re.match(r"lea rcx, \[(rsp|rbp) ([+-]) (0x[0-9a-f]+|\d+)\]$", rd)
    cls, how = "DYNAMIC", rd
    if m:
        base, off = m.group(1), (1 if m.group(2) == "+" else -1) * int(m.group(3), 0)
        pat = re.compile(r"mov dword ptr \[%s ([+-]) (0x[0-9a-f]+|\d+)\], (.+)$" % base)
        consts = {}
        for x in ins[:-1]:
            t = "%s %s" % (x.mnemonic, x.op_str)
            mm = re.match(r"mov (e\w+|r\d+d), (0x[0-9a-f]+|\d+)$", t)
            if mm:
                consts[mm.group(1)] = int(mm.group(2), 0)
            elif x.op_str and x.op_str.split(",")[0].strip() in consts and x.mnemonic not in ("cmp", "test"):
                consts.pop(x.op_str.split(",")[0].strip(), None)
            ms = pat.match(t)
            if ms and (1 if ms.group(1) == "+" else -1) * int(ms.group(2), 0) == off:
                v = ms.group(3).strip()
                if re.match(r"^(0x[0-9a-f]+|\d+)$", v):
                    cls, how = "CONST %d" % int(v, 0), t
                elif v in consts:
                    cls, how = "CONST %d" % consts[v], t + " (%s = %d)" % (v, consts[v])
                else:
                    cls, how = "DYNAMIC", t
    rows.append(("%08X" % site, "%08X" % fa, cls, how, rd))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rc1_records_%08X.tsv" % TARGET)
with io.open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write("site\tfunction\tclass\tlast_class_store\trcx_definition\n")
    for r in rows:
        f.write("\t".join(r) + "\n")
for r in rows:
    print("\t".join(r))
