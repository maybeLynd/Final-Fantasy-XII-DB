"""EQ-1 control (OPUS, 2026-09-27): which of the 28 st2e group slots at 02EC3D80 can ever be loaded.

G1  every slot 0..27 has one setter `mov [02EC3D80 + 8*slot], rdx`, and 002FA560(group) selects slot group's setter
    and tail-jumps 002385D0(group, setter).
G2  002385D0 reads the loader id from the byte table 01E09F68[group] and returns without a request when it is
    negative (js at 002385EE); otherwise 00384420(id, setter, ...).
G3  01E09F68: group 0 is -1 (never loadable); every other group has a non-negative loader id.
G4  loads are on demand: 002F8040(group) is `slot != null`, and the only requesters of 002FA560 are 00248700 (group
    from its record +0xC8, when 002F8040 says not loaded) and 0053EB90 (groups 0x19 and 0x1A explicitly).
Mutant M1: flipping group 7's byte to 0xFF makes G3's loadable set lose slot 7.
"""
import hashlib, pathlib, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE.parents[3] / "Tools" / "work" / "exe" / "FFXII_TZA.exe"
raw = EXE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
pe = pefile.PE(data=raw, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
md = Cs(CS_ARCH_X86, CS_MODE_64)
def at(va, n, buf=raw): o = pe.get_offset_from_rva(va - IB); return buf[o:o + n]
def dis(a, n): return list(md.disasm(at(a, n), a))
BASE = 0x2EC3D80
# G1: 002FA560's arms
arms = {}
ins = dis(0x2FA560, 476)
for k, i in enumerate(ins):
    if i.mnemonic == "lea" and i.op_str.startswith("rdx, [rip"):
        tgt = i.address + i.size + int(i.op_str.split("0x")[1].rstrip("]"), 16) * (1 if "+" in i.op_str else -1)
        grp = None
        for j in ins[max(0, k - 3):k][::-1]:
            if j.mnemonic == "cmp" and j.op_str.startswith("ecx, "): grp = int(j.op_str.split(", ")[1], 0); break
            if j.mnemonic == "test" and j.op_str == "ecx, ecx": grp = 0; break
        arms[grp] = tgt
assert sorted(arms) == list(range(28)), sorted(arms)
for g, s in arms.items():
    si = dis(s, 16)
    store = next(i for i in si if i.mnemonic == "mov" and i.op_str.startswith("qword ptr [rip"))
    slot_va = store.address + store.size + int(store.op_str.split("0x")[1].split("]")[0], 16)
    assert slot_va == BASE + 8 * g and store.op_str.endswith("rdx"), (g, hex(slot_va))
# G2
g2 = {i.address: (i.mnemonic, i.op_str) for i in dis(0x2385D0, 102)}
assert g2[0x2385E8][0] == "movzx" and g2[0x2385EE] == ("js", "0x23862e") and g2[0x23861E] == ("call", "0x384420")
# G3
def loadable(buf):
    t = at(0x1E09F68, 28, buf)
    return {g for g in range(28) if t[g] < 0x80}
L = loadable(raw)
assert L == set(range(1, 28)), sorted(set(range(28)) - L)
mut = bytearray(raw); o = pe.get_offset_from_rva(0x1E09F68 + 7 - IB); mut[o] = 0xFF
assert 7 not in loadable(bytes(mut))                        # M1
# G4
g4 = [(i.mnemonic, i.op_str) for i in dis(0x2F8040, 20)]
assert ("cmp", "qword ptr [rcx + rdx*8], rax") in g4 and ("setne", "al") in g4
req = [(i.address, i.mnemonic, i.op_str) for i in dis(0x53EB90, 0x120)]
assert any(a == 0x53EC64 and o == "ecx, 0x19" for a, m, o in req) and any(a == 0x53EC7A and o == "ecx, 0x1a" for a, m, o in req)
t = at(0x1E09F68, 28)
null_at_title = [0, 7, 8, 11, 15, 16, 21, 22, 24, 25, 26, 27]            # EXP-002
print("never loadable:", [g for g in null_at_title if g not in L])
print("loadable on demand, null at title:", [(g, t[g]) for g in null_at_title if g in L])
print("PASS")
