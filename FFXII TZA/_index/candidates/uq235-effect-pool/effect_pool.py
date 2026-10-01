"""effect_pool.py - UQ-235 second half: what the class-8 state query 00375AE0 and release 00375470 do
(FABLE, Claude Opus 5.5, 2026-09-26).

The screen-effect pool is 32 records of 0x70 bytes at 02EBF9E0: the descriptor copied in whole at +0x00..+0x67,
the handle at +0x68, an elapsed counter at +0x6C.
  E1 both class dispatchers reach the two bodies by a bare tail jump in their class-8 slot (0024DE9F jmp 00375AE0,
     0024D01F jmp 00375470), so neither does anything before or after them.
  E2 00375AE0 matches the handle at +0x68 and dispatches on kind byte +0: kind 0 -> 0; kind 1 -> 5 when +0x24 <= +0x6C,
     otherwise 3; kinds 2, 3, 5, 6 and 13 -> 3; kinds 4 and 7-12 are passed over and the walk goes on; not found -> 0.
  E3 00375470 scans the handles to the first empty one (the pool is kept packed). It removes the match by moving
     the later records down one (rep movsq of (31 - i) * 0x70 bytes) and zeroing 02EC07D8, which is record 31's
     handle (02EBF9E0 + 31 * 0x70 + 0x68).
  E4 writes: 00375AE0 has none; 00375470 has exactly the rep movsq into the pool and the 02EC07D8 store. The
     planted positive: the enumerator must see that store.
  E5 the counter: the allocator 00375900 zeroes +0x6C and copies the descriptor with six 16-byte moves and one
     8-byte move (+0x00..+0x67), so descriptor offsets are record offsets. The pool tick 00374950 adds 1 or 2 to
     +0x6C, and for kind 1 calls 00374060 and then releases the record through 00375470 when that returns 0.
     00374060 returns 0 when +0x1C bit 1 is set and +0x24 < +0x6C.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

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
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))   # bounded by functions.tsv body_bytes
def S(a, size): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in ins(a, size)}
def u32(v): return struct.unpack_from("<I", d, off(v))[0]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

POOL, END = 0x2EBF9E0, 0x2EBF9E0 + 32 * 0x70
check("E1 class-8 slots are bare tail jumps",
      BASE + u32(0x24DEAC + 4 * 7) == 0x24DE9F and S(0x24DE9F, 5)[0x24DE9F] == "jmp 0x375ae0"
      and BASE + u32(0x24D02C + 4 * 7) == 0x24D01F and S(0x24D01F, 5)[0x24D01F] == "jmp 0x375470")
Q = S(0x375AE0, 0x59)
tbl = [BASE + u32(0x375B3C + 4 * k) for k in range(14)]
want = {0: 0x375B18, 1: 0x375B1B, 2: 0x375B33, 3: 0x375B33, 5: 0x375B33, 6: 0x375B33, 13: 0x375B33}
for k in (4, 7, 8, 9, 10, 11, 12): want[k] = 0x375B0F
check("E2 state query kind table", tbl == [want[k] for k in range(14)] and Q[0x375AFD] == "cmp edx, 0xd",
      " ".join("%d:%X" % (k, t) for k, t in enumerate(tbl)))
check("E2 kind 1: 5 when +0x24 <= +0x6C else 3; kinds 2/3/5/6/13: 3; not found: 0",
      Q[0x375B1B] == "mov ecx, dword ptr [rax + 0x6c]" and Q[0x375B1E] == "mov edx, 3"
      and Q[0x375B23] == "cmp dword ptr [rax + 0x24], ecx" and Q[0x375B26] == "mov r8d, 5"
      and Q[0x375B2C] == "cmovbe edx, r8d" and Q[0x375B33] == "mov eax, 3" and Q[0x375B18] == "xor eax, eax"
      and Q[0x375AF5] == "cmp dword ptr [rax + 0x68], ecx")
R = S(0x375470, 0x87)
check("E3 release: stop at first empty handle, shift (31-i) records, clear record 31's handle",
      R[0x375492] == "test edx, edx" and R[0x375494] == "je 0x3754ec" and R[0x3754CF] == "mov eax, 0x1f"
      and R[0x3754D7] == "imul rcx, rax, 0x70" and R[0x3754DF].startswith("rep movsq")
      and 0x3754E2 + 10 + struct.unpack_from("<i", d, off(0x3754E2) + 2)[0] == POOL + 31 * 0x70 + 0x68)
def writes(a, size):
    out = []
    for x in ins(a, size):
        if x.mnemonic.startswith("rep movs"): out.append((x.address, "rep movsq -> pool")); continue
        ops = x.operands
        if ops and ops[0].type == X86_OP_MEM and x.mnemonic in ("mov", "add", "sub", "and", "or", "xor", "inc", "dec", "movups", "movsd", "movaps"):
            m = ops[0].mem
            if m.base == 0 or cs.reg_name(m.base) != "rsp":
                tgt = x.address + x.size + m.disp if cs.reg_name(m.base) == "rip" else None
                out.append((x.address, "%s %s" % (x.mnemonic, x.op_str), tgt))
    return out
wq, wr = writes(0x375AE0, 0x59), writes(0x375470, 0x87)
check("E4 state query writes nothing", wq == [], str(wq))
check("E4 release writes only the pool shift and record 31's handle (planted positive: the store is seen)",
      [w[0] for w in wr] == [0x3754DF, 0x3754E2] and wr[1][2] == POOL + 31 * 0x70 + 0x68, str(wr))
A = S(0x375900, 0x120)
T = S(0x374950, 0x95); K = S(0x374060, 0x50)
check("E5 allocator zeroes +0x6C and copies +0x00..+0x67 straight",
      A.get(0x3759C2) == "mov dword ptr [rcx + 0x6c], 0" and A.get(0x3759F7) == "movsd xmm0, qword ptr [rbx + 0x60]"
      and A.get(0x375A01) == "movsd qword ptr [rcx + 0x60], xmm0"
      and all(A.get(a) == "movups xmmword ptr [rcx%s], xmm%d" % ("" if o == 0 else " + 0x%x" % o, r)
              for a, o, r in ((0x3759CC, 0, 0), (0x3759D3, 0x10, 1), (0x3759DB, 0x20, 0), (0x3759E3, 0x30, 1), (0x3759EB, 0x40, 0), (0x3759F3, 0x50, 1))))
check("E5 tick advances +0x6C by 1 or 2; kind 1 -> 00374060, released through 00375470 on 0",
      T[0x3749A2] == "add dword ptr [rbx + 0x6c], eax" and T[0x374996] == "mov eax, 1" and T[0x37499D] == "mov eax, 2"
      and T[0x3749A5] == "movzx ecx, byte ptr [rbx]" and T[0x3749A8] == "sub ecx, 1" and T[0x3749B0] == "call 0x374060"
      and T[0x3749BC] == "call 0x375470")
check("E5 00374060: release when +0x1C bit 1 and +0x24 < +0x6C",
      K[0x37408F] == "test byte ptr [rbx + 0x1c], 2" and K[0x374095] == "mov eax, dword ptr [rbx + 0x6c]"
      and K[0x374098] == "cmp dword ptr [rbx + 0x24], eax" and K[0x37409B] == "jae 0x3740a5" and K[0x37409D] == "xor eax, eax")
print("FAILS", fails)
sys.exit(1 if fails else 0)
