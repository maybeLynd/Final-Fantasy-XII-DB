"""uq213_programs.py - UQ-213: the VU1 microprograms this image uses, and the primitive each draws
(FABLE, Claude Opus 5.5, 2026-09-27). Static; checks uq213-programs.tsv against the bytes and the published tables.
  U1 the four registrars 003A34D0 / 003A33B0 (program in r9) and 003A35E0 / 003A2F70 (program in r8) have 104 direct
     call sites; the program argument at each is a `lea` from rip; they register 44 distinct programs.
  U2 the template table's mpg_program column names 35; the union is 57 and the rows of uq213-programs.tsv are exactly
     those 57; the region table's microprogram rows all fall inside it.
  U3 the ten programs registered only through 003A33B0 / 003A2F70 - the difference between 57 and the page's 47 -
     are 00499A20 0049B9E0 0049D540 004A0090 004A1E30 004A33B0 004A4410 004A8B00 004AAFC0 004B0230.
  U4 control: for the programs whose template tag the page already decoded, the row's primitive agrees with
     members/vif1-gif-tags.tsv (0x68 / 0x69 second programs 004E0F70 / 004DDDF0 triangle strip 0x05C; 0xA3's 004DB350
     line 0x049; 0xA9's 00479650 triangle strip 0x05C).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
REG = {0x3A34D0: "r9", 0x3A33B0: "r9", 0x3A35E0: "r8", 0x3A2F70: "r8"}
sites = []; progs = {}
for f in sorted(SIZES):
    if not 0x121000 <= f < 0x8C0000 or SIZES[f] <= 0: continue
    o = off(f)
    if o is None: continue
    blob = d[o:o + SIZES[f]]
    if not any(b == 0xE8 for b in blob): continue
    L = None
    for i in range(len(blob) - 4):
        if blob[i] != 0xE8: continue
        t = f + i + 5 + struct.unpack_from("<i", blob, i + 1)[0]
        if t not in REG: continue
        if L is None: L = list(cs.disasm(blob, f))
        k = next((j for j, x in enumerate(L) if x.address == f + i), None)
        if k is None or L[k].mnemonic != "call": continue
        reg = REG[t]; p = None
        for y in reversed(L[max(0, k - 60):k]):      # backward slice through register copies
            if y.op_str.startswith(reg + ","):
                m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", y.op_str)
                if y.mnemonic == "lea" and m: p = y.address + y.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)); break
                m2 = re.fullmatch(r"r\w+, (r\w+)", y.op_str)
                if y.mnemonic == "mov" and m2: reg = m2.group(1); continue
                break
        sites.append((f + i, t, p)); progs.setdefault(p, set()).add(t)
reg_progs = {p for p in progs if p is not None}
check("U1 104 registrar call sites, each passing a rip-formed program; 44 distinct programs",
      len(sites) == 104 and None not in progs and len(reg_progs) == 44, "sites %d, programs %d, unresolved %d" % (len(sites), len(reg_progs), len(progs.get(None, ()))))
tmpl = {int(r["mpg_program"], 16) for r in csv.DictReader(open(DB / "17-Presentation-Rendering/Legacy-PS2-GS/vif1-packet-templates.tsv", encoding="utf-8"), delimiter="\t") if r.get("mpg_program")}
rows = {int(r["program"], 16): r for r in csv.DictReader(open(HERE / "uq213-programs.tsv", encoding="utf-8"), delimiter="\t")}
region = {int(r["address"], 16) for r in csv.DictReader(open(DB / "17-Presentation-Rendering/Legacy-PS2-GS/members/vu1-region-functions.tsv", encoding="utf-8"), delimiter="\t") if r["role"].startswith("microprogram")}
union = reg_progs | tmpl
check("U2 templates name 35; the union is 57 and is exactly the table's rows; the region table's microprograms are inside it",
      len(tmpl) == 35 and len(union) == 57 and set(rows) == union and region <= union,
      "templates %d, union %d, rows %d, region %d outside %s" % (len(tmpl), len(union), len(rows), len(region), sorted("%08X" % a for a in region - union)))
only_b = {p for p in reg_progs if progs[p] <= {0x3A33B0, 0x3A2F70}} - tmpl
ten = {0x499A20, 0x49B9E0, 0x49D540, 0x4A0090, 0x4A1E30, 0x4A33B0, 0x4A4410, 0x4A8B00, 0x4AAFC0, 0x4B0230}
check("U3 the ten registered only through 003A33B0 / 003A2F70 are the difference from 47", only_b == ten and len(union) - len(ten) == 47,
      sorted("%08X" % a for a in only_b ^ ten))
ctl = {0x4E0F70: "0x05C", 0x4DDDF0: "0x05C", 0x4DB350: "0x049", 0x479650: "0x05C"}
bad = {"%08X" % p: rows[p]["draws"][:40] for p, prim in ctl.items() if p not in rows or prim not in rows[p]["draws"]}
gif = [r for r in csv.DictReader(open(DB / "17-Presentation-Rendering/Legacy-PS2-GS/members/vif1-gif-tags.tsv", encoding="utf-8"), delimiter="\t")]
page = {r["prim_raw"] for r in gif if r["builder"] in ("004E2930", "004DCA00", "004DC6B0")}
check("U4 control: the four already-decoded programs carry the page's primitives", not bad and {"0x05C", "0x049"} <= page, "%s; page tags %s" % (bad, sorted(page)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
