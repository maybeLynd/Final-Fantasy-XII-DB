"""select_mmsg_receivers.py [--write] - EC-7 selector for the 28 MMSG message
value receiver adapters (SWE2-EC7, 2026-09-16;
FABLE-REQ-SWE2-EC7-MMSG-RECEIVER-ADAPTERS-B).

Members are derived, not listed: the selector disassembles the per-kind
dispatcher 002FA560 and takes its 28 LEA targets - exactly the adapter set
FABLE found. Each member is then required to be EXACTLY:

    movsxd rdx, ecx            ; sign-extend the incoming value
    mov    ecx, K              ; (K = 0 uses xor ecx, ecx)
    mov    [rip + 02EC3D80 + K*8], rdx   ; store into slot K of the group table
    jmp    00238640            ; forward (K, value) to the per-kind record fixup

Controls printed and asserted before writing:
  - 002FA560 yields exactly 28 lea targets, all census entries;
  - 28 of 28 match the four-instruction form, K = 0..0x1B contiguous, all
    globals the consecutive 02EC3D80+8K slots, all tails 00238640;
  - near-miss rejection: every other census entry in 002F7000-002F8000 that
    is NOT a lea target of 002FA560 fails the form check (a body that is
    merely nearby, or four instructions without this exact shape, stays out).

The dispatcher's own role is documented on the binmenu page: 002FA560(k, cb)
routes through 002385D0 and the byte table 01E09F68 to register cb under the
'MMSG' tag at 00914698. This row disposes of the 28 adapters only; 002385D0,
00384420, 00238640, 003845F0 and the record table 02F973C0 stay untouched.

Inputs (gitignored, reproducible): Tools/work/exe/FFXII_TZA.exe,
graph/functions.tsv; needs capstone."""
import sys, os, struct, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
W = os.path.normpath(os.path.join(DB, "..", "Tools", "work"))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd

IMG = 0x120000
d = open(os.path.join(W, "exe", "FFXII_TZA.exe"), "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = {}
for i in range(n):
    o = pe + 24 + opt + i * 40
    nm = d[o:o + 8].rstrip(b"\0").decode(); vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs[nm] = (IMG + va, vs, ro, rs)
def off(a):
    for va, vs, ro, rs in secs.values():
        if va <= a < va + rs: return ro + (a - va)

sizes = cd.load_functions(); eset = set(sizes)
a_set = cd.measure_a(DB, sizes)[0]
declared = {}
for doc, parts in cd.parse_families(DB):
    if len(parts) >= 5 and parts[1] in cd.LETTERS:
        try:
            for m in cd.read_members(doc, parts[2]): declared[m] = parts[0]
        except Exception:
            pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True

def dis(e): return list(md.disasm(d[off(e):off(e) + sizes[e]], e))
def mem_g(x):
    for op in x.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP and op.mem.index == 0:
            return x.address + x.size + op.mem.disp

def member_form(e):
    """return (k, global) iff e is exactly the adapter form, else None"""
    if sizes[e] > 24: return None
    ins = dis(e)
    if len(ins) != 4: return None
    i0, i1, i2, i3 = ins
    if not (i0.mnemonic == "movsxd" and i0.op_str == "rdx, ecx"): return None
    if i1.mnemonic == "mov" and i1.operands[0].type == X86_OP_REG \
       and md.reg_name(i1.operands[0].reg) == "ecx" and i1.operands[1].type == X86_OP_IMM:
        k = i1.operands[1].imm & 0xFFFFFFFF
    elif i1.mnemonic == "xor" and i1.op_str == "ecx, ecx":
        k = 0
    else:
        return None
    if not (i2.mnemonic == "mov" and i2.op_str.startswith("qword ptr [rip")
            and i2.op_str.endswith("], rdx")): return None
    g = mem_g(i2)
    if g != 0x2EC3D80 + 8 * k: return None
    if not (i3.mnemonic == "jmp" and i3.op_str == "0x238640"): return None
    return k, g

# seed: the dispatcher's lea targets
tgts = set()
for x in dis(0x2FA560):
    if x.mnemonic == "lea":
        g = mem_g(x)
        if g is not None and g in eset: tgts.add(g)
assert len(tgts) == 28, "002FA560 must lea exactly 28 adapter bodies"

members = {}
for t in sorted(tgts):
    r = member_form(t)
    if r is not None: members[t] = r
assert len(members) == 28, "28 of 28 lea targets must pass the form check"
assert sorted(k for k, _ in members.values()) == list(range(0x1C)), "k must be 0..0x1B"
assert len({g for _, g in members.values()}) == 28

# near-miss control: no other census body in the neighbourhood passes
near = [e for e in eset if 0x2F7000 <= e < 0x2F8000 and e not in tgts]
reject = [e for e in near if member_form(e) is not None]
assert not reject, "near-miss bodies must not pass: %s" % reject
print("002FA560 lea targets: 28, all census; form 28/28; k = 0..0x1B contiguous;")
print("  globals 02EC3D80+8k all distinct; all tails jmp 00238640")
print("  near-miss control: %d neighbour bodies in 002F7000-002F8000 tested, %d pass (0 required)"
      % (len(near), len(reject)))
excl = [t for t in tgts if t in a_set or t in declared]
print("  declared/A overlap: %d" % len(excl))

if "--write" in sys.argv:
    out = os.path.join(HERE, "mmsg-value-receiver-adapters.tsv")
    with open(out, "w", newline="\n") as f:
        f.write("# MMSG message value receiver adapters: movsxd rdx,ecx ; mov ecx,k|xor ; mov [rip+02EC3D80+8k],rdx ; jmp 00238640 - select_mmsg_receivers.py\n")
        f.write("address\tk\tglobal\tsize\n")
        for t, (k, g) in sorted(members.items()):
            f.write("%08X\t%d\t%08X\t%d\n" % (t, k, g, sizes[t]))
    print("wrote", len(members))
