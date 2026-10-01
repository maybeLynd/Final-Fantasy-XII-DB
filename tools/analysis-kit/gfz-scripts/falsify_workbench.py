"""Falsification pass 1 on CONTRACT-shared-transform-workbench (OPUS, 2026-09-29), from the shipping image. Killers first.

  W1  TW-1: 022D8F00 and 022D9500 both lie past .data's SizeOfRawData
  W2  TW-2: over every rip-relative access into 022D8F00..022D9500, the 16-byte-wide ones touch 46 distinct addresses, all
      16-byte aligned; the number of 16-byte-wide access sites is reported beside the page's 3,892
  W3  TW-3: 003970A0 is 44 B and does four movups loads from 022D91B0 / C0 / D0 / E0 and four stores to [rcx + 0 .. 0x30]
  W4  TW-4: 267 functions touch the region, 249 write it, 18 only read; 16 of those read only 022D94B0 / 022D94B4, one reads
      only 022D8F0C (00501820), one reads matrix rows (003970A0)
  W5  TW-6: no rip-relative store to 022D94B0 / 022D94B4 exists; the indexed stores are 0036DE5A / 0036DF6A (`mov word [r9 + rdx*8], r10w`, r9 = lea
      022D94B4) and 0036E2F8 (`or byte [rax + rdx + 0x10], dil`, rax = lea 022D94B0)
"""
import collections, io, os
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
text = next(x for x in SECS if x[0] == ".text")
LO, HI = 0x022D8F00, 0x022D9500
touch = collections.defaultdict(lambda: {"w": False, "r": set()})
w16, s16, lea_tab, store_tab = set(), 0, [], []
WR = ("mov", "movss", "movups", "movaps", "movdqu", "movdqa", "movsd", "or", "and", "add", "sub", "inc", "dec", "xor")
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    for x in md.disasm(code, fa):
        for k, o in enumerate(x.operands):
            if o.type != X86_OP_MEM or o.mem.base != X86_REG_RIP:
                continue
            t = x.address + x.size + o.mem.disp
            if not (LO <= t < HI):
                continue
            wr = k == 0 and x.mnemonic in WR
            if wr:
                touch[fa]["w"] = True
            elif x.mnemonic != "lea" or True:
                touch[fa]["r"].add(t)
            if o.size == 16:
                w16.add(t); s16 += 1
            if t in (0x022D94B0, 0x022D94B4):
                if x.mnemonic == "lea":
                    lea_tab.append((x.address, t))
                if wr:
                    store_tab.append(x.address)
data = next(x for x in SECS if x[0] == ".data")
raw_end = data[1] + data[4]
check("W1", LO >= raw_end and HI >= raw_end, ".data raw data ends %08X" % raw_end)
check("W2", len(w16) == 46 and all(a % 16 == 0 for a in w16), "%d distinct 16-byte addresses, all aligned; %d 16-byte-wide access sites (the page says 3,892)" % (len(w16), s16))
g = list(md.disasm(blob[OFF(0x003970A0):OFF(0x003970A0) + sizes[0x003970A0]], 0x003970A0))
loads = sorted(x.address + x.size + o.mem.disp for x in g if x.mnemonic == "movups" for o in x.operands[1:] if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP)
stores = sorted(o.mem.disp for x in g if x.mnemonic == "movups" for o in x.operands[:1] if o.type == X86_OP_MEM and x.reg_name(o.mem.base) == "rcx")
check("W3", sizes[0x003970A0] == 44 and loads == [0x022D91B0, 0x022D91C0, 0x022D91D0, 0x022D91E0] and stores == [0, 0x10, 0x20, 0x30],
      "44 B; loads %s; stores [rcx + %s]" % (["%08X" % l for l in loads], [hex(s) for s in stores]))
ro = [f for f, v in touch.items() if not v["w"]]
tab = [f for f in ro if touch[f]["r"] <= {0x022D94B0, 0x022D94B4}]
others = sorted((("%08X" % f), sorted("%08X" % t for t in touch[f]["r"])) for f in ro if f not in tab)
check("W4", len(touch) == 267 and sum(1 for v in touch.values() if v["w"]) == 249 and len(ro) == 18 and len(tab) == 16
      and others == [("003970A0", ["022D91B0", "022D91C0", "022D91D0", "022D91E0"]), ("00501820", ["022D8F0C"])],
      "%d functions, %d writers, %d read-only (%d table-only); others %s" % (len(touch), sum(1 for v in touch.values() if v["w"]), len(ro), len(tab), others))
ini = {x.address: S(x) for x in md.disasm(blob[OFF(0x0036D9E0):OFF(0x0036D9E0) + 2400], 0x0036D9E0)}
check("W5", not store_tab and ini.get(0x0036DE5A) == "mov word ptr [r9 + rdx*8], r10w" and ini.get(0x0036DF6A) == "mov word ptr [r9 + rdx*8], r10w"
      and ini.get(0x0036E2F8) == "or byte ptr [rax + rdx + 0x10], dil" and {t for _a, t in lea_tab} == {0x022D94B0, 0x022D94B4},
      "no rip store to the table base; the cited sites are the indexed stores %s / %s / %s; bases reached only by lea"
      % (ini.get(0x0036DE5A), ini.get(0x0036DF6A), ini.get(0x0036E2F8)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
