"""GI-7 checks (FABLE 2026-09-29): bank B of the authored presentation commands is a one-slot bank for command 5.

B1  every rip-relative reference into bank B 02CA4670..02CA48C8 (and the context cell 02CA4668 beside it), over every
    listed function: expected exactly the boot clear 0041CCA0 (lea), the registrar 0041D6D0 (lea) and one read, the id-5
    invoker 00417C60 loading slot 5 (02CA4698). Positive control: the same scan finds the id-5 invoker's bank-A slot-5
    read (02CA4438) in 00417C60.
B2  no image-base-relative displacement 0x2B84670..0x2B848C8 anywhere (control: 0x29CA030 is found).
B3  raw E8/E9 callers of the registrar 0041D6D0: exactly one, at 00426A1C inside CharacterRenderSystem_Initialize 004269A0,
    preceded by `lea ecx, [rdi + 5]` and `lea rdx` -> 00520C50.
B4  pair table 01EFFAF0 slot 5 = {00417C60, flag 1}.
B5  both actor-side registrars store the empty stub 0016D6A0 in bank-A slot 5 (002EA320 at 002EA492, 002EA5F0 at 002EA5FB).
Exit 1 on any failure.
"""
import struct, sys, bisect
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((d[o:o + 8].rstrip(b"\0"), va, ro, rs))
text = [s for s in secs if s[0] == b".text"][0]


def off(va):
    rva = va - BASE
    for _n, a, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


funcs = {}
for ln in open(FUNCS, encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    if p[0] != "entry":
        funcs[int(p[0], 16)] = int(p[2])
starts = sorted(funcs)
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
fails = []
rip_hits, disp_hits, ctl_disp = [], [], []
for fn in starts:
    if not (text[1] <= fn - BASE < text[1] + text[3]):
        continue
    o = off(fn)
    for x in md.disasm(d[o:o + funcs[fn]], fn):
        for op in x.operands:
            if op.type != X86_OP_MEM:
                continue
            if op.mem.base and x.reg_name(op.mem.base) == "rip":
                t = x.address + x.size + op.mem.disp
                if 0x02CA4430 <= t < 0x02CA48C8:
                    rip_hits.append((x.address, fn, t, x.mnemonic))
            else:
                if 0x2B84670 <= op.mem.disp < 0x2B848C8:
                    disp_hits.append(x.address)
                if op.mem.disp == 0x29CA030:
                    ctl_disp.append(x.address)
bankb = sorted({(fn, t, m) for a, fn, t, m in rip_hits if t >= 0x02CA4668})
print("B1 references into 02CA4668..02CA48C8:")
for fn, t, m in bankb:
    print("   %08X in %08X  %s" % (t, fn, m))
want = {(0x0041CCA0, 0x02CA4670, "lea"), (0x0041D6D0, 0x02CA4670, "lea"), (0x00417C60, 0x02CA4698, "mov")}
b_only = {r for r in bankb if r[1] != 0x02CA4668}
ok1 = b_only == want and any(fn == 0x00417C60 and t == 0x02CA4438 for _a, fn, t, _m in rip_hits)
print("B1", "OK" if ok1 else "FAIL", "(control: bank-A slot 5 read in 00417C60 found)" if ok1 else "")
if not ok1:
    fails.append("B1")
ok2 = not disp_hits and bool(ctl_disp)
print("B2 image-base-relative hits:", disp_hits, "control hits:", len(ctl_disp), "OK" if ok2 else "FAIL")
if not ok2:
    fails.append("B2")
lo = off(BASE + text[1])
callers = []
for i in range(lo, lo + text[3] - 5):
    if d[i] in (0xE8, 0xE9):
        src = BASE + text[1] + (i - lo)
        if src + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x0041D6D0:
            callers.append(src)
print("B3 raw callers of 0041D6D0:", ["%08X" % c for c in callers])
ok3 = callers == [0x00426A1C]
if ok3:
    seq = list(md.disasm(d[off(0x00426A12):off(0x00426A12) + 10], 0x00426A12))
    ok3 = (seq[0].mnemonic == "lea" and seq[0].address + seq[0].size + seq[0].operands[1].mem.disp == 0x00520C50
           and seq[1].op_str == "ecx, [rdi + 5]")
print("B3", "OK" if ok3 else "FAIL")
if not ok3:
    fails.append("B3")
inv, fl = struct.unpack_from("<QI", d, off(0x01EFFAF0) + 5 * 16)
ok4 = inv == 0x00417C60 and fl == 1
print("B4 pair table slot 5 = %08X flag %d" % (inv, fl), "OK" if ok4 else "FAIL")
if not ok4:
    fails.append("B4")
ok5 = True
for site in (0x002EA492, 0x002EA5FB):
    prev = [x for x in md.disasm(d[off(site - 0x0E):off(site) + 5], site - 0x0E)]
    lea = [x for x in prev if x.mnemonic == "lea" and x.op_str.startswith("rdx")]
    tgt = lea[-1].address + lea[-1].size + lea[-1].operands[1].mem.disp if lea else None
    mov = [x for x in prev if x.address == site]
    good = tgt == 0x0016D6A0 and mov and mov[0].op_str == "ecx, 5"
    print("B5 %08X: rdx -> %s, %s" % (site, "%08X" % tgt if tgt else "?", mov[0].op_str if mov else "?"), "OK" if good else "FAIL")
    ok5 = ok5 and bool(good)
if not ok5:
    fails.append("B5")
print("FAILS", len(fails), fails)
sys.exit(1 if fails else 0)
