"""bit46_regindex.py - the register-index form bit46_writers.py cannot see: an index 46 (0x2E) placed in a register
(mov r32, 0x2E) and used within the next 8 instructions by bt/bts/btr/btc r64,reg, shl/shlx/sal/rol of a 64-bit
register, or as cl. Lists every such pair image-wide. Control: a synthetic byte string with `mov ecx, 0x2e;
mov eax, 1; shl rax, cl` must be found by the same matcher. FABLE, 2026-09-30."""
import sys, struct, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
d = tk.d
BASE = 0x00120000
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
for i in range(nsec):
    s = pe + 24 + opt + 40 * i
    if d[s:s + 8].rstrip(b"\0") == b".text":
        vs, va, rs, ro = struct.unpack_from("<IIII", d, s + 8)
blob = d[ro:ro + rs]
R32 = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
R64 = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esp": "rsp", "ebp": "rbp", "esi": "rsi", "edi": "rdi"}
def uses(x, reg32):
    r64 = R64.get(reg32, reg32.rstrip("d"))
    ops = [o.strip() for o in x.op_str.split(",")]
    if x.mnemonic in ("bt", "bts", "btr", "btc") and len(ops) == 2 and ops[1] in (reg32, r64): return True
    if x.mnemonic in ("shl", "sal", "rol", "shlx", "sarx", "shrx") and (reg32 == "ecx" and ops[-1] == "cl" or ops[-1] in (reg32, r64)):
        return True
    return False
def scan(buf, base_addr):
    out = []
    for p in range(len(buf) - 6):
        b = buf[p]
        pre = 0
        if b == 0x41: pre = 1; b = buf[p + 1]
        if 0xB8 <= b <= 0xBF and buf[p + 1 + pre:p + 5 + pre] == b"\x2e\x00\x00\x00":
            reg = (R32[b - 0xB8] if not pre else "r%dd" % (8 + b - 0xB8))
            a = base_addr + p
            seq = list(md.disasm(buf[p:p + 64], a, 9))
            if not seq or seq[0].address != a or seq[0].mnemonic != "mov": continue
            for x in seq[1:]:
                if uses(x, reg): out.append((a, x)); break
    return out
ctl = scan(b"\xb9\x2e\x00\x00\x00\xb8\x01\x00\x00\x00\x48\xd3\xe0" + b"\x90" * 64, 0x1000)
print("CONTROL synthetic mov ecx,0x2e; mov eax,1; shl rax,cl:", "PASS" if ctl else "FAIL")
hits = scan(blob, BASE + va)
print("image-wide register-index uses of 0x2E: %d" % len(hits))
for a, x in hits:
    o, _ = tk.owner(a)
    print("  %08X mov ..., 0x2e -> %08X %s %s   in %s" % (a, x.address, x.mnemonic, x.op_str, tk.fname(o)))
print("FAILS %d" % (0 if ctl else 1))
