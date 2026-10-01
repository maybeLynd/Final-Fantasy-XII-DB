"""ph2_header_swap_members.py - PH-2: what 0063E2E0 swaps when it is handed the PClusterHeader descriptor 02CAA0A0
(FABLE, Claude Opus 5.5, 2026-09-26). The member reading is OPUS's s49-header-i1-static-bound.md (2026-09-25); this
control re-derives it from the bytes and adds who runs the registrations.

  P1 the parent chain. The three descriptor constructors pass constant (size, base) pairs to 00632D80:
     02CAA0A0 PClusterHeader       00597690  size 0x54  base 02CA9DA0
     02CA9DA0 PClusterHeaderD3D11  005977E0  size 0x54  base 02CA9FA0
     02CA9FA0 PClusterHeaderBase   00597730  size 0x48  base 006372A0() (the root)
  P2 the members. 005983E0 makes 18 calls to the member registrar 00632960 onto 02CA9FA0, and 00598C50 makes 3 onto
     02CA9DA0. Every call takes its type from 00630180. The offsets are 0x00..0x44 and 0x48, 0x4C, 0x50: 21 dwords,
     0x54 bytes, which is the header size.
  P3 PClusterHeader itself registers nothing. No call to 00632960 in 005983E0, 00598C50 or 0059D550 passes 02CAA0A0.
     Image-wide, in .text no `lea rdx, [rip+d32]` aimed at 02CAA0A0 is followed within 0x40 bytes by a 00632960 call.
     The same sweep on 02CA9FA0 finds exactly 005983E0's 18. Blind spot: a descriptor pointer that reaches rdx some
     other way (a register copy, a load) is not covered.
  P4 the swap leaf. 00630180 returns the type singleton 01F2E5A0. vtable 00D311B0 is installed on it, and slot 0 of
     that vtable is 005CB140 = 8B 02 0F C8 89 02 B0 01 C3 (bswap the dword at rdx, return 1).
  P5 who runs the registrations. 0059D550 calls 005983E0 and 00598C50. It is slot +0x08 of vtable 00D26C40, whose
     RTTI locator names PSerialization::PUtilitySerialization. The static initialiser 00160320 installs that vtable
     on 01F2CD80 and links the object into the module chain at 02CACC90. The engine-init walker 005A08E0 calls slot
     +0x08 of every object on that chain (005A0A39). Its one direct caller is 007980A0.
  Control: the same member parse applied to 00598DF0 (the third call in 0059D550) finds its registrations onto a
     different descriptor, 02CA9EA0, and none onto the three header descriptors. So the parse sees registrations when
     they are there.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG, X86_REG_RIP
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
def txt(L): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in L}
def q(a): return struct.unpack_from("<Q", d, off(a))[0]
def rip(x):
    for o in x.operands:
        if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP: return x.address + x.size + o.mem.disp
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

def ctor(a):
    """(size, base) passed to 00632D80: r9d immediate and the qword stored at [rsp+0x28]."""
    L = ins(a, 0x60); size = base = None
    for x in L:
        if x.mnemonic == "mov" and x.op_str.startswith("r9d, "): size = x.operands[1].imm
        if x.mnemonic == "lea" and x.op_str.startswith("rax, [rip"): base = rip(x)
        if x.mnemonic == "call" and x.op_str == "0x6372a0": base = "root"
        if x.mnemonic == "call" and x.op_str == "0x632d80": return size, base
C = {0x597690: ctor(0x597690), 0x5977E0: ctor(0x5977E0), 0x597730: ctor(0x597730)}
check("P1 the parent chain PClusterHeader -> PClusterHeaderD3D11 -> PClusterHeaderBase -> root, sizes 0x54/0x54/0x48",
      C[0x597690] == (0x54, 0x2CA9DA0) and C[0x5977E0] == (0x54, 0x2CA9FA0) and C[0x597730] == (0x48, "root"),
      str({"%08X" % k: v if not isinstance(v[1], int) else (hex(v[0]), "%08X" % v[1]) for k, v in C.items()}))

def regs(a, size):
    """every 00632960 call in the body: (descriptor, offset, type-from-00630180)."""
    out = []; desc = offv = None; typ = False; regs0 = {}
    for x in ins(a, size):
        s = "%s %s" % (x.mnemonic, x.op_str)
        if x.mnemonic == "xor" and len(x.operands) == 2 and x.operands[0].type == X86_OP_REG and x.operands[0].reg == x.operands[1].reg:
            regs0[x.reg_name(x.operands[0].reg)] = 0
        if x.mnemonic == "call" and x.op_str == "0x630180": typ = True
        if x.mnemonic == "lea" and x.op_str.startswith("rdx, [rip"): desc = rip(x)
        if x.mnemonic == "mov" and x.op_str.startswith("dword ptr [rsp + 0x20], "):
            src = x.operands[1]
            offv = src.imm if src.type == X86_OP_IMM else regs0.get(x.reg_name(src.reg))
        if x.mnemonic == "call" and x.op_str == "0x632960":
            out.append((desc, offv, typ)); desc = offv = None; typ = False
    return out
B = regs(0x5983E0, 0x865); D3 = regs(0x598C50, 0x200)
offs = sorted(o for _, o, _ in B + D3)
check("P2 005983E0 registers 18 members onto 02CA9FA0 at 0x00..0x44",
      len(B) == 18 and all(ds == 0x2CA9FA0 and t for ds, _, t in B) and sorted(o for _, o, _ in B) == list(range(0, 0x48, 4)),
      "n=%d offsets %s" % (len(B), [hex(o) if o is not None else None for _, o, _ in B]))
check("P2 00598C50 registers 3 members onto 02CA9DA0 at 0x48, 0x4C, 0x50",
      len(D3) == 3 and all(ds == 0x2CA9DA0 and t for ds, _, t in D3) and sorted(o for _, o, _ in D3) == [0x48, 0x4C, 0x50],
      "n=%d" % len(D3))
check("P2 the 21 dwords cover 0x00..0x53 exactly once: 0x54 bytes, the PClusterHeader size",
      offs == list(range(0, 0x54, 4)) and len(offs) * 4 == C[0x597690][0])
R = txt(ins(0x59D550, 0x39))
check("P3 PClusterHeader registers nothing: no 00632960 call onto 02CAA0A0, and 0059D550 makes none itself",
      all(ds != 0x2CAA0A0 for ds, _, _ in B + D3) and "call 0x632960" not in R.values())
# P3, image-wide: every `lea rdx, [rip+d32]` (48 8D 15) in .text aimed at the descriptor, followed by a call to
# 00632960 within 0x40 bytes. Control: the same sweep on 02CA9FA0 must find 005983E0's 18.
text = [(BASE + va, rs, ro) for vs, va, rs, ro in secs][0]
def sweep(target):
    hits = []; tb, trs, tro = text; k = d.find(b"\x48\x8D\x15", tro)
    while 0 <= k < tro + trs:
        a = tb + k - tro
        if a + 7 + struct.unpack_from("<i", d, k + 3)[0] == target:
            L = ins(a, 0x40)
            if L and L[0].address == a and any(x.mnemonic == "call" and x.op_str == "0x632960" for x in L): hits.append(a)
        k = d.find(b"\x48\x8D\x15", k + 1)
    return hits
H0, H1 = sweep(0x2CAA0A0), sweep(0x2CA9FA0)
check("P3 image-wide: no `lea rdx, [02CAA0A0]` precedes a 00632960 call; control 02CA9FA0 finds its 18",
      H0 == [] and len(H1) == 18 and all(0x5983E0 <= a < 0x5983E0 + 0x865 for a in H1),
      ".text %08X+%X; header hits %d, base hits %d" % (text[0], text[1], len(H0), len(H1)))
leaf = q(0xD311B0)
V = {x.address: x for x in ins(0x63167C, 14)}
check("P4 00630180 returns 01F2E5A0; 006315B0 stores vtable 00D311B0 there; its slot 0 = 005CB140 = bswap dword [rdx]; return 1",
      any(rip(x) == 0x1F2E5A0 for x in ins(0x630180, 0x40) if x.mnemonic == "lea")
      and V[0x63167C].mnemonic == "lea" and rip(V[0x63167C]) == 0xD311B0
      and V[0x631683].mnemonic == "mov" and rip(V[0x631683]) == 0x1F2E5A0 and V[0x631683].op_str.endswith("rax")
      and leaf == 0x5CB140 and d[off(0x5CB140):off(0x5CB140) + 9] == bytes.fromhex("8B020FC889 02B001C3".replace(" ", "")))
def rtti(col):
    td = BASE + struct.unpack_from("<IIII", d, off(col))[3]
    s = d[off(td) + 16:off(td) + 200]; return s[:s.find(b"\0")].decode()
I = txt(ins(0x160320, 0x56)); W = txt(ins(0x5A08E0, 507))
check("P5 0059D550 = slot +0x08 of PUtilitySerialization's vtable 00D26C40; installed by 00160320 and linked at 02CACC90",
      q(0xD26C48) == 0x59D550 and rtti(q(0xD26C38)) == ".?AVPUtilitySerialization@PSerialization@Phyre@@"
      and R.get(0x59D554) == "call 0x5983e0" and R.get(0x59D559) == "call 0x598c50"
      and any(rip(x) == 0xD26C40 for x in ins(0x160320, 0x56) if x.mnemonic == "lea")
      and any(rip(x) == 0x2CACC90 for x in ins(0x160320, 0x56)), rtti(q(0xD26C38)))
check("P5 the engine-init walker 005A08E0 calls slot +0x08 down the chain from 02CACC90",
      W.get(0x5A0A39) == "call qword ptr [rax + 8]" and any(rip(x) == 0x2CACC90 for x in ins(0x5A08E0, 507)))
X = regs(0x598DF0, 0x800)
check("control: the same parse finds 00598DF0's registrations, onto 02CA9EA0 and not onto a header descriptor",
      len(X) > 0 and all(ds == 0x2CA9EA0 for ds, _, _ in X), "n=%d descriptors %s" % (len(X), sorted({"%08X" % ds for ds, _, _ in X if ds})))
print("FAILS", fails)
sys.exit(1 if fails else 0)
