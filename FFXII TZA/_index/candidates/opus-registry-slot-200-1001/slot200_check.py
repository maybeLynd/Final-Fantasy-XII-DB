"""slot200_check.py - registry slot 0x02EBF200 (license_board): what it holds and who reads it (OPUS, 2026-10-01).
Static, the certified image (Tools/work/exe/FFXII_TZA.exe), capstone. Prints PASS/FAIL lines and FAILS n.

S1  00236C30 stores field +0x11C of the 0208E680 record RAW into 02EBF200 (movsxd + mov qword, 0023702A / 00237031),
    not through the registrar 003845F0(&slot, field) that binds its neighbours (control: the 02EBF008 slot at 00237010).
S2  rip-relative census over the whole image: 02EBF200..02EBF207 has exactly one reference, that write
    (positive control: the neighbour 02EBF1F8 shows a read at 002385A9).
S3  every indexed access through the job-board base 02EBF1A0 is bounded to slots 0..11 (02EBF1A0..02EBF1F8):
    00233E00 (cl <= 0xB; the count loop stops before 02EBF208, last read rcx+0x20 = 02EBF1F8), 002368D0 (rep stosq,
    ecx = 0xC), 00237630 / 00238260 (cl <= 0xB), 00328990 (r8d <= 0xB).
"""
import os, struct, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
base = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + 40 * i
    name = d[o:o + 8].rstrip(b"\0").decode()
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, base + va, vs, ro, rs))
text = [s for s in secs if s[0] == ".text"][0]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = False
fails = 0


def check(name, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + name)
    fails += 0 if ok else 1


def dis(va, n):
    off = text[3] + (va - text[1])
    return list(md.disasm(d[off:off + 16 * n], va, n))


def rip_target(ins):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", ins.op_str)
    if not m:
        return None
    disp = int(m.group(2), 16)
    return ins.address + ins.size + (disp if m.group(1) == "+" else -disp)


# S1
w = dis(0x0023702A, 2)
check("S1 0023702A movsxd rcx, dword [rax+0x11c]", w[0].mnemonic == "movsxd" and "0x11c" in w[0].op_str)
check("S1 00237031 mov qword [02EBF200], rcx", w[1].address == 0x00237031 and w[1].mnemonic == "mov" and rip_target(w[1]) == 0x02EBF200)
c = dis(0x00237010, 3)
check("S1 control: 02EBF008 goes through the registrar 003845F0", rip_target(c[0]) == 0x02EBF008 and c[2].mnemonic == "call"
      and c[2].op_str == "0x3845f0")

# S2: linear sweep of .text for rip-relative references into [LO, HI]
refs = {}
off0 = text[3]; va0 = text[1]; size = min(text[2], text[4])
pos = 0
md.skipdata = True
for ins in md.disasm(d[off0:off0 + size], va0):
    t = rip_target(ins)
    if t is not None and 0x02EBF1F8 <= t <= 0x02EBF207:
        refs.setdefault(t & ~7, []).append((ins.address, ins.mnemonic, ins.op_str))
r200 = refs.get(0x02EBF200, [])
check("S2 02EBF200 has exactly one rip reference, the write at 00237031", [a for a, _, _ in r200] == [0x00237031])
r1f8 = refs.get(0x02EBF1F8, [])
check("S2 control: 02EBF1F8 shows the read at 002385A9", any(a == 0x002385A9 and m == "mov" and o.startswith("rcx") for a, m, o in r1f8))

# S3: index bounds on the job-board base
g = dis(0x00233E00, 3)
check("S3 00233E00 bounds cl <= 0xB", g[0].op_str == "cl, 0xb" and g[1].mnemonic == "ja")
lp = dis(0x00233E24, 30)
lea_end = [i for i in lp if i.mnemonic == "lea" and rip_target(i) == 0x02EBF208]
step = [i for i in lp if i.mnemonic == "add" and i.op_str == "rcx, 0x30"]
far = [i for i in lp if "[rcx + 0x20]" in i.op_str]
check("S3 00233E00 loop: start 02EBF1A8, step 0x30, stop before 02EBF208, widest read rcx+0x20 -> last slot 02EBF1F8",
      rip_target(lp[0]) == 0x02EBF1A8 and lea_end and step and far and (0x02EBF1A8 + 0x30) + 0x20 == 0x02EBF1F8)
z = dis(0x002369E5, 6)
check("S3 002368D0 rep stosq over 12 qwords from 02EBF1A0", rip_target(z[0]) == 0x02EBF1A0 and any(i.op_str == "ecx, 0xc" for i in z)
      and any(i.mnemonic.startswith("rep stosq") or i.mnemonic == "rep stosq" for i in z))
h = dis(0x00237630, 3)
check("S3 00237630 bounds cl <= 0xB", h[1].op_str == "cl, 0xb" and h[2].mnemonic == "ja")
k = dis(0x00238304, 2)
check("S3 00238260 bounds cl <= 0xB before 00238319", k[0].op_str == "cl, 0xb" and k[1].mnemonic == "ja")
q = dis(0x003289A4, 2)
check("S3 00328990 bounds r8d <= 0xB", q[0].op_str == "r8d, 0xb" and q[1].mnemonic == "ja")
print("FAILS %d" % fails)
