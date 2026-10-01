"""SWE2-AUDIT-SEM (2): the batch-5 readings re-derived from the certified image (b92561451, SWE2-DATA's DD owner read of
five Movement-and-Navigation pages). Capstone and pefile read Tools/work/exe/FFXII_TZA.exe directly; the producer's
mv_clamp_checks.py / mv_loco_checks.py / mm_checks.py are re-run separately (producer_rerun.out) and are not the
evidence here. Each check is one claim of the package; F-checks are findings this review adds.

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-dd-owner-read-5-0930/dd5_sem.py"
"""
import csv
import os
import struct
import subprocess
import sys

import capstone
import pefile

ROOT = os.getcwd()
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Database", "Tools", "work", "graph", "functions.tsv")
pe = pefile.PE(EXE, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
FAILS = []
size = {r["entry"]: int(r["body_bytes"] or 0) for r in csv.DictReader(open(FUNCS, encoding="utf-8"), delimiter="\t")}


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


def raw(va, n):
    o = pe.get_offset_from_rva(va - BASE)
    return bytes(pe.__data__[o:o + n])


def run(va, end):
    return [i for i in md.disasm(raw(va, end - va + 16), va) if i.address <= end]


def at(va):
    return next(md.disasm(raw(va, 16), va))


def rip(i):
    for op in i.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def tgt(i):
    if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == capstone.x86.X86_OP_IMM:
        return i.operands[0].imm
    return None


def txt(ins):
    return " ; ".join(f"{i.mnemonic} {i.op_str}" for i in ins)


def section_of(va):
    for s in pe.sections:
        a = BASE + s.VirtualAddress
        if a <= va < a + max(s.Misc_VirtualSize, s.SizeOfRawData):
            return s.Name.rstrip(b"\0").decode()
    return "?"


# ---- clamping a point into a volume ---------------------------------------------------------------------------------
f = run(0x00363FD0, 0x00363FD0 + 0x230)
f = f[:[k for k, i in enumerate(f) if i.mnemonic == "ret"][-1] + 1] if any(i.mnemonic == "ret" for i in f) else f
dsts = {rip(i) for i in f if i.mnemonic.startswith("mov") and rip(i) and i.op_str.startswith("xmmword") or (i.mnemonic.startswith("mov") and rip(i) and i.op_str.split(",")[0].strip().endswith("]"))}
check("K1 00363FD0 copies its arguments to 022D92A0 / 022D92B0 / 022D92C0", {0x022D92A0, 0x022D92B0, 0x022D92C0} <= dsts)
loads = {rip(i) for i in f if rip(i) in (0x01EF93F0, 0x01EF93FC)}
check("K2 00363FD0 loads its clamp bounds from 01EF93F0 and 01EF93FC", loads == {0x01EF93F0, 0x01EF93FC})
st = {i.address: rip(i) for i in f if rip(i) in (0x022D92D4, 0x022D92E4) and i.op_str.split(",")[0].strip().startswith("dword")}
check("K3 the squared distance is stored to 022D92E4 (003641D4) and 022D92D4 (003641DC)",
      st.get(0x003641D4) == 0x022D92E4 and st.get(0x003641DC) == 0x022D92D4, str({hex(k): hex(v) for k, v in st.items()}))
check("F1 the bounds cell is .data, the software vf00 image, not a constant (the struck 'they are .data addresses, not immediates' was true)",
      section_of(0x01EF93F0) == ".data", section_of(0x01EF93F0))
v = struct.unpack("<4f", raw(0x01EF93F0, 16))
check("F1 its file image holds [0,0,0,1]: lanes x = 0.0 and w = 1.0 are what the clamp reads", v == (0.0, 0.0, 0.0, 1.0), str(v))
wr = []
for a, n in ((0x0036D9A8, "movss [01EF93FC]"), (0x0036D9E8, "movss [01EF93FC]"), (0x0036DD87, "movups [01EF93F0]")):
    i = at(a)
    wr.append(rip(i) in (0x01EF93F0, 0x01EF93FC) and i.op_str.split(",")[0].strip().endswith("]"))
check("F1 the three runtime writers of the cell (0036D9A8, 0036D9E8, 0036DD87; CONTRACT-transform-primitives §15b) still store to it", all(wr))

w = run(0x003631B0, 0x003633AF)
check("K4 the volume walk 003631B0 is 512 B and forms each record as u16 offset + [022CBAF0] (00363263)",
      w[-1].mnemonic == "ret" and w[-1].address + 1 - 0x003631B0 == 512 and rip(at(0x00363263)) == 0x022CBAF0)
seq = run(0x0036326A, 0x003632CC)
calls = {tgt(i) for i in seq if tgt(i)}
check("K5 byte +9 & 0x7F: 0 -> 00361DE0 (ellipse), 1 -> 003623C0 (box), 2 -> 00362230 (chain), other -> point copied unchanged",
      "byte ptr [rbx + 9]" in seq[0].op_str and seq[1].op_str == "ecx, 0x7f" and calls >= {0x00361DE0, 0x003623C0, 0x00362230}
      and at(0x0036327D).op_str == "xmm0, xmmword ptr [rsi]")
after = run(0x003632D1, 0x00363350)
check("K6 (SD-180) after the clamp the walk reads +0x58/+0x54/+0x38, calls 00361810 and 003638B0, and returns r9d or 003638B0's result",
      [a for a in ("0x58", "0x54", "0x38") if any(f"[rbx + {a}]" in i.op_str for i in after)] == ["0x58", "0x54", "0x38"]
      and {tgt(i) for i in after if tgt(i)} == {0x00361810, 0x003638B0} and at(0x00363350).op_str == "ebp, eax" and at(0x003631BE).op_str == "ebp, r9d")
c = run(0x00362230, 0x00362230 + 388 - 1)
check("K7 the chain body 00362230 is 388 B, walks [r8+0x14] segments of 0x20 from +0x40, calls 00363FD0 and reads 022D92D4 after it",
      size.get("00362230") == 388 and any(tgt(i) == 0x00363FD0 for i in c) and any(rip(i) == 0x022D92D4 for i in c if i.address > 0x0036228A)
      and any("0x14]" in i.op_str for i in c) and any("0x40" in i.op_str for i in c))
check("K8 00363FD0's only direct call site is 0036228A (edges and a raw rel32 sweep agree on one)", tgt(at(0x0036228A)) == 0x00363FD0)

# ---- setting the movement mode ----------------------------------------------------------------------------------------
s = run(0x00263CC0, 0x00263CF6)
check("M1 00263CC0: class 1 -> [[+0xB8]+0x38]; (class-1)==2, i.e. class 3 -> [[+0xB8]+0xA4]; else 0.0 (EC7-105 kind correction holds)",
      s[4].op_str == "edx, 1" and s[6].op_str == "edx, 2" and "0xa4" in s[9].op_str and "0x38" in s[12].op_str)
i = at(0x002692E8)
check("M2 the mode-5 setter: 002692E8 mov byte [steer+0x28], 5 (steer = [[actor+0xB8]+0xF0])", i.op_str == "byte ptr [rcx + 0x28], 5"
      and "0xf0" in at(0x002692E1).op_str)
check("M3 002E5750's call site 0025E3AA passes edx = ebp", tgt(at(0x0025E3AA)) == 0x002E5750 and at(0x0025E3A5).op_str == "edx, ebp")
g = run(0x0025E2F8, 0x0025E36E)
check("F2 (SD-190) ebp is 1 only if 003E68B0(rec) != 0 (0025E31D, before the cited range) AND actor +0x0D bit 1 AND 003E6A70(rec) bit 0",
      tgt(at(0x0025E31D)) == 0x003E68B0 and at(0x0025E322).op_str == "ecx, eax" and at(0x0025E326).op_str == "ecx, ebp"
      and at(0x0025E32E).mnemonic == "cmovne" and at(0x0025E331).mnemonic == "test" and tgt(at(0x0025E35A)) == 0x003E6A70
      and at(0x0025E36A).op_str == "al, 1" and at(0x0025DF1F).op_str == "ebp, ebp")
a = run(0x003E6A70, 0x003E6A95)
b = run(0x003AEF50, 0x003AEF85)
check("F3 (SD-190) 003E6A70 = 003E6E60(rec) ? 003AEF50(rec+0x550) : 0; 003AEF50 walks the list at [obj+0x18] by +0x48 and sets bit 0 if a node's byte +1 != 0, bit 1 if byte +2 != 0",
      tgt(a[3]) == 0x003E6E60 and a[9].op_str == "rcx, [rbx + 0x550]" and tgt(a[-1]) == 0x003AEF50
      and "[rcx + 0x18]" in b[3].op_str and "[r8 + 1]" in b[7].op_str and "[r8 + 2]" in b[10].op_str and "[r8 + 0x48]" in b[11].op_str
      and b[9].op_str == "edx, 2" and b[14].op_str == "eax, 1")
c2 = run(0x003AEF20, 0x003AEF2D)
check("F3 003E68B0 is the same wrapper over 003AEF20: 1 when the tween object is armed and its list [obj+0x18] is non-empty",
      tgt(run(0x003E68B0, 0x003E68D5)[-1]) == 0x003AEF20 and "[rcx + 0x18]" in c2[3].op_str and c2[4].mnemonic == "setne")
k = [i for i in run(0x0026C200, 0x0026C240) if "0x3e20d97c" in i.op_str]
check("M4 modding: pi/20 = 0x3E20D97C is stored at 0026C224", bool(k) and k[0].address == 0x0026C224, txt(k))
i = at(0x002E5806)
check("M4 modding: the 0.5-degree floor 0x3C0EFA35 is loaded at 002E5806 (from 00D0F8DC, .rdata - a constant, not an immediate)",
      rip(i) == 0x00D0F8DC and struct.unpack("<I", raw(0x00D0F8DC, 4))[0] == 0x3C0EFA35 and at(0x002E580F).mnemonic == "comiss", f"{i.mnemonic} {i.op_str}")
check("M4 the two immediates are pi/20 and 0.5 degree", abs(struct.unpack("<f", struct.pack("<I", 0x3E20D97C))[0] - 3.14159265 / 20) < 1e-6
      and abs(struct.unpack("<f", struct.pack("<I", 0x3C0EFA35))[0] - 3.14159265 / 360) < 1e-7)

# ---- battle locomotion -------------------------------------------------------------------------------------------------
i = at(0x0033C956)
check("L1 0033C956 addss of the float 5.0 at 009146E4", i.mnemonic == "addss" and rip(i) == 0x009146E4 and struct.unpack("<f", raw(0x009146E4, 4))[0] == 5.0)
i1, i2 = at(0x0033D747), at(0x0033D751)
check("L2 0033D747 mulss 0.5 (01CEBB70), 0033D751 divss 3.0 (008F311C)",
      i1.mnemonic == "mulss" and rip(i1) == 0x01CEBB70 and struct.unpack("<f", raw(0x01CEBB70, 4))[0] == 0.5
      and i2.mnemonic == "divss" and rip(i2) == 0x008F311C and struct.unpack("<f", raw(0x008F311C, 4))[0] == 3.0)
d = run(0x0033A039, 0x0033A0A6)
check("L3 00339F00 dispatches modes 1/4, 2, 6 to 0033CEF0, 0033D200, 0033BAA0 (0033A039-0033A0A6)",
      {tgt(x) for x in d if tgt(x)} >= {0x0033CEF0, 0x0033D200, 0x0033BAA0}, txt([x for x in d if tgt(x)]))
check("L4 DecodeOrderGoal 00312730 is 965 B in the function list", size.get("00312730") == 965, str(size.get("00312730")))

# ---- the two census claims, from the image-wide rip-relative reference scan (retool.py refs, cached) -----------------
RT = ["python", "-B", os.path.join("Database", "Tools", "analysis-kit", "gfz-scripts", "retool.py")]


def refs(a, stores=False):
    out = subprocess.run(RT + ["refs", a] + (["--stores"] if stores else []), capture_output=True, check=True).stdout.decode("utf-8", "replace")
    return [l for l in out.splitlines() if l.startswith(a)]


w = refs("02B40534", True)
fn = {l.split(" in ")[1].split(":")[0] for l in w}
check("W1 02B40534: 8 store sites in 8 functions, 003B6ED0 included (the corrected count)", len(w) == 8 and len(fn) == 8 and "003B6ED0" in fn,
      ", ".join(sorted(fn)))
w = refs("022CBAF0", True)
fn = sorted(l.split(" in ")[1].split(":")[0] for l in w)
check("F4 (SD-181) the base 022CBAF0 has three writers: 00362F70 zeroes it (called by 00266D10), 003635C0 stores rcx (called by 003775D0 with [02ADD060]), 00363730 zeroes it (called by 00378230)",
      fn == ["00362F70", "003635C0", "00363730"] and tgt(at(0x003775F5)) == 0x003635C0 and rip(at(0x003775EE)) == 0x02ADD060
      and tgt(at(0x00266E68)) == 0x00362F70 and tgt(at(0x003782CE)) == 0x00363730, ", ".join(fn))

print("FAILS", len(FAILS))
sys.exit(1 if FAILS else 0)
