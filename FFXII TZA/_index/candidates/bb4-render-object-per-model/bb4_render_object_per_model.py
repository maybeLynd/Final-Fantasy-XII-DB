"""bb4_render_object_per_model.py - BB-4: a CharacterRenderObject is acquired per character render record and
recycled per model; it is not shared (FABLE, Claude Opus 5.5, 2026-09-26). Static reads of the shipping image, plus
the model-id decoder 002ED6F0 executed under Unicorn.

  A1 acquire 001BD4A0(pool, id): looks the id's model entry up (001BAFF0) and searches the pool tree for the entry's
     +0x2A0. On a HIT it takes the first object of that node's list ([node+0x30] -> [+0x10]), runs ResetState
     (001F89E0), unlinks and frees the list element (0x20 bytes), and erases the node when its list is empty
     (001BCFB0). On a MISS it allocates 0x668, constructs, and calls slot 2 with (id, entry). Both paths append the
     object to the active vector at pool +8. So a pooled object is handed to ONE acquirer and leaves the pool.
  A2 release 001BD840(pool, obj): finds obj in the active vector, computes its key with 001F6E60 = [[obj+0x488]+0x2A0],
     find-or-inserts the tree node for that key (001BCE30), appends an element {obj, 3}, and removes obj from the vector.
  A3 the acquirers are character render records: Skeleton_UpdateFinalPoseAndCombatLook (003703A0) and 0053AB50 run,
     when record +0x6B8 is null and 0017EFC0(record +0x6B0) reports the model entry present,
     record +0x6B8 = 0017F0D0(record +0x6B0) (a tail jump to the acquire); CharacterRenderRecord_TeardownAndReset
     (004200A0) passes record +0x6B8 to 0017F100 (a tail jump to the release) and zeroes it.
  A4 the pool key: the asset loader 001BB2B0 decodes the id with 002E98F0 / 002ED6F0 and stores
     +0x2A0 = (kind << 32) | index (001BB736-001BB745); executed, 'c' 1004 -> (14, 25100), 'm' 1004 -> (34, 11044).
  A5 sensitivity: the "shared thereafter" reading needs the hit path to return the node's object without taking it
     out of the node; the bytes unlink it (the two stores at 001BD58D / 001BD597) and free the element (001BD5A8).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RSP
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

f = dis(0x1BD4A0, 0x1BD4A0 + 0x17D)
hit = (f.get(0x1BD566) == "mov rax, qword ptr [rbx + 0x30]" and f.get(0x1BD56A) == "mov rsi, qword ptr [rax + 0x10]"
       and f.get(0x1BD579) == "call 0x1f89e0" and f.get(0x1BD5A2) == "mov r8d, 0x20" and f.get(0x1BD5A8) == "call qword ptr [rax + 0x18]"
       and f.get(0x1BD5CE) == "call 0x1bcfb0")
miss = (f.get(0x1BD527) == "mov ecx, 0x668" and f.get(0x1BD53E) == "call 0x1f4da0" and f.get(0x1BD561) == "call qword ptr [rax + 0x10]"
        and f.get(0x1BD564) == "jmp 0x1bd5d3")
vec = f.get(0x1BD5D3) == "mov rdx, qword ptr [rbp + 8]" and f.get(0x1BD5ED) == "mov qword ptr [rdx], rsi"
check("A1 acquire: a hit takes a pooled object out of its node; a miss constructs; both join the active vector",
      hit and miss and vec and f.get(0x1BD4D3) == "call 0x1baff0")
r = dis(0x1BD840, 0x1BD840 + 0xF4); k = dis(0x1F6E60, 0x1F6E6F)
check("A2 release: key = [[obj+0x488]+0x2A0]; the object goes back into that key's list and leaves the vector",
      r.get(0x1BD898) == "call 0x1f6e60" and r.get(0x1BD89D) == "lea rcx, [rsi + 0x20]" and r.get(0x1BD8AB) == "call 0x1bce30"
      and r.get(0x1BD890) == "mov dword ptr [rsp + 0x28], 3" and r.get(0x1BD902) == "add qword ptr [rsi + 8], -8"
      and list(k.values())[:2] == ["mov rax, qword ptr [rcx + 0x488]", "mov rax, qword ptr [rax + 0x2a0]"])
s1 = dis(0x3704C2, 0x3704F6); s2 = dis(0x53AC9D, 0x53ACD7); t = dis(0x4200F8, 0x420118)
w1 = dis(0x17F0D0, 0x17F0FC); w2 = dis(0x17F100, 0x17F133)
check("A3 the acquirers and the releaser are character render records (+0x6B0 model id, +0x6B8 object)",
      s1.get(0x3704C2) == "cmp qword ptr [rsi + 0x6b8], 0" and s1.get(0x3704D2) == "call 0x17efc0" and s1.get(0x3704E1) == "call 0x17f0d0"
      and s1.get(0x3704E6) == "mov qword ptr [rsi + 0x6b8], rax"
      and s2.get(0x53AC9D) == "cmp qword ptr [r12 + 0x6b8], rbx" and s2.get(0x53ACC0) == "call 0x17f0d0"
      and t.get(0x4200F8) == "mov rcx, qword ptr [rbx + 0x6b8]" and t.get(0x4200FF) == "call 0x17f100"
      and t.get(0x42010B) == "mov qword ptr [rbx + 0x6b8], rdi"
      and w1.get(0x17F0F1) == "jmp 0x1bd4a0" and w2.get(0x17F128) == "jmp 0x1bd840")
m = dis(0x1BB727, 0x1BB750); e = dis(0x2E98F0, 0x2E9918)
mu = Uc(UC_ARCH_X86, UC_MODE_64)
for vs, va, rs, ro in secs:
    a = BASE + va; size = (max(vs, rs) + 0xFFF) & ~0xFFF
    mu.mem_map(a, size); mu.mem_write(a, d[ro:ro + min(rs, vs if vs else rs)])
mu.mem_map(BASE, 0x1000); mu.mem_write(BASE, d[:0x1000])
STK, RET = 0x70000000, 0x60000000
mu.mem_map(STK, 0x10000); mu.mem_map(RET, 0x1000); mu.mem_write(RET, b"\xC3")
def dec(i):
    mu.mem_write(STK + 0x100, struct.pack("<II", 0xAAAAAAAA, 0xBBBBBBBB))
    mu.reg_write(UC_X86_REG_RCX, i); mu.reg_write(UC_X86_REG_RDX, STK + 0x100); mu.reg_write(UC_X86_REG_R8, STK + 0x104)
    mu.reg_write(UC_X86_REG_RSP, STK + 0x8000); mu.mem_write(STK + 0x8000, struct.pack("<Q", RET))
    mu.emu_start(0x2ED6F0, RET, count=200)
    return struct.unpack("<II", bytes(mu.mem_read(STK + 0x100, 8)))
L = lambda ch, num: (ord(ch) << 16) | num
check("A4 the pool key is the model's resource identity (kind, index) decoded from the id",
      m.get(0x1BB745) == "mov qword ptr [rax + 0x2a0], rdx" and m.get(0x1BB73A) == "shl rdx, 0x20" and e.get(0x2E9900) == "call 0x2ed6f0"
      and dec(L("c", 1004)) == (14, 25100) and dec(L("m", 1004)) == (34, 11044) and dec(L("c", 1004)) != dec(L("c", 1005)),
      repr((dec(L("c", 1004)), dec(L("m", 1004)))))
check("A5 sensitivity: the hit path unlinks the pooled element (so no two acquirers get one object)",
      f.get(0x1BD58D) == "mov qword ptr [rcx], rax" and f.get(0x1BD597) == "mov qword ptr [rcx + 8], rax")
print("FAILS", fails)
sys.exit(1 if fails else 0)
