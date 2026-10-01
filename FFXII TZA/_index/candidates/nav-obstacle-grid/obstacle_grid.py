"""obstacle_grid.py - what occupies the nav grid, end to end (FABLE, Claude Opus 5.5, 2026-09-28), on
ASTRA-REQ-FABLE-NAV-POPULATION-DOMAINS. Decoded from the certified image's bytes.

  B1 the builder 00392740 resets the count 02AEE0BC to 0 before its null-grid test, then clears the cell records
     (memset [02AEE0A0], cells * n), the occupancy bytes (memset [02AEE0A8], cells) and the 0x400-byte list at 02AEE0C0
  B2 phase 1: for groups 0, 1, 2 it walks the actor-manager slot range (00263FF0, 00263C50(g, 3), 00263B50(g, 3)) and fetches
     each actor (00358940); while count < 0x80 it stores the actor at list[count] (0039286E), takes position and two radii
     (002646C0, 00265090), and rasterizes it with id = count; ids 0..127
  B3 phase 2: the dataset root's records (count min(root+0x24, 0x20), 0x20-byte stride) get ids from 0x80: ids 128..159
  B4 phase 3: registry entries i < n get id 0xA0 + i (003929BD lea ecx, [rsi + 0xa0]), n read through 0032A6B0 twice when the
     first read is below 0x80 (0039298D / 00392991): ids 160..287 while n <= 128
  R1 the rasterizer 00392200(id, x, z, r) clamps the square [x - r, x + r] x [z - r, z + r] to the grid, tests each cell with
     004690B0, and on a hit sets bit id of the cell's n-byte record (byte cell * n + id / 8, bts id & 7) and increments the
     cell's occupancy byte ([02AEE0A8] + cell, a u8 inc)
  W  n = 0x24 (003924CB) is 288 bits = 0x80 + 0x20 + 0x80 ids exactly; id 288 would address byte n of a cell record - the next
     cell's first byte, or the first occupancy byte after the last cell
  Q1 the query 00391710 walks the mask for ids 0 .. count - 1 only (count = [02AEE0BC], the listed actors): for each set bit
     it takes list[id] (02AEE0C0), gets its bounds (002FB340) and tests them against the query shape (00468A70); ids 128..287 do
     not reach its result
  C  controls: the three id bases are read from the image, not assumed (a planted lea ecx, [rsi + 0xa1] moves B4's base);
     the bit arithmetic model with n = 0x24 puts id 287 in the cell and id 288 outside it
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + 40 * i + 8) for i in range(ns)]
off = lambda v: next(ra + v - 0x120000 - va for vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def body(img, a, n):
    ins = list(MD.disasm(img[off(a):off(a) + n], a))
    assert ins[-1].address + ins[-1].size == a + n, "%08X extent" % a
    return {i.address: (i.mnemonic + " " + i.op_str).strip() for i in ins}
def rip(a, b):
    """rip-relative target of the instruction at a in body b."""
    m = re.search(r"rip \+ 0x(\w+)\]", b[a]); nxt = min(x for x in b if x > a)
    return nxt + int(m.group(1), 16) if m else None
P = body(d, 0x392740, 702)
ok("B1", P[0x392777] == "mov dword ptr [rip + 0x275b93f], esi" and rip(0x392777, P) == 0x2AEE0BC and P[0x392780] == "je 0x3929e8"
   and P[0x3927BB] == "call 0x861ec0" and rip(0x39275A, P) == 0x2AEE0A0 and rip(0x3927CF, P) == 0x2AEE0A8 and P[0x3927D9] == "call 0x861ec0"
   and rip(0x3927E0, P) == 0x2AEE0C0 and P[0x3927E7] == "mov r8d, 0x400" and P[0x3927ED] == "call 0x861ec0",
   "count reset before the null-grid test; records, occupancy bytes and the 0x400-byte list cleared")
ok("B2", P[0x392808] == "call 0x263ff0" and P[0x392817] == "call 0x263c50" and P[0x392826] == "call 0x263b50" and P[0x392847] == "call 0x358940"
   and P[0x392865] == "cmp eax, ebp" and P[0x3927FF] == "mov ebp, 0x80" and P[0x39286E] == "mov qword ptr [rsi + rax*8], rdi"
   and P[0x39287F] == "call 0x2646c0" and P[0x392891] == "call 0x265090" and P[0x3928B4] == "call 0x392200" and P[0x3928DD] == "cmp r13d, 3",
   "three groups; guard count < 0x80 before list[count] = actor; position, max of two radii; id = count")
ok("B3", P[0x392904] == "mov edx, 0x20" and P[0x39290C] == "cmovb edx, dword ptr [rax + 0x24]" and P[0x392917] == "mov ebx, ebp" and P[0x39295E] == "add rdi, 0x20"
   and P[0x392957] == "call 0x392200", "dataset records: count min(root+0x24, 0x20), stride 0x20, ids from 0x80")
ok("B4", P[0x392968] == "call 0x32a6b0" and P[0x39298D] == "cmp eax, ebp" and P[0x39298F] == "jge 0x392998" and P[0x392991] == "call 0x32a6b0"
   and P[0x392996] == "mov ebp, eax" and P[0x3929BD] == "lea ecx, [rsi + 0xa0]" and P[0x3929D5] == "call 0x392200",
   "registry: n = 0x80 when the first read >= 0x80, else a second read used unchecked; id = 0xA0 + i")
R = body(d, 0x392200, 679)
ok("R1", R[0x3923CD] == "call 0x4690b0" and R[0x3923D4] == "je 0x39242e" and R[0x3923F0] == "sar r8d, 3" and R[0x3923EB] == "and eax, 7"
   and R[0x3923FD].startswith("imul ecx, dword ptr [rip") and rip(0x3923FD, R) == 0x2AEE0B8 and R[0x39240F] == "bts ecx, eax"
   and R[0x392412] == "mov byte ptr [r8 + rdx], cl" and rip(0x392424, R) == 0x2AEE0A8 and R[0x39242B] == "inc byte ptr [rcx + rax]",
   "on a circle-cell hit: bit id of record byte cell*n + id/8 set; the cell's occupancy byte incremented")
G = body(d, 0x3924B0, 607)
n = struct.unpack_from("<I", d, off(0x3924CB) + 6)[0]
def byte_of(cell, i, n=n): return cell * n + (i >> 3)
ok("W", G[0x3924CB] == "mov dword ptr [rip + 0x275bbe3], 0x24" and n == 0x24 and 0x80 + 0x20 + 0x80 == n * 8
   and byte_of(0, 287) == n - 1 and byte_of(0, 288) == n,
   "n = 0x%X: %d bits = 128 + 32 + 128 ids; id 287 in byte %d, id 288 in byte %d = the next cell's first" % (n, n * 8, byte_of(0, 287), byte_of(0, 288)))
Q = body(d, 0x391710, 0x3919A3 - 0x391710)
ok("Q1", rip(0x3918DC, Q) == 0x2AEE0BC and rip(0x3918F1, Q) == 0x2AEE0C0 and Q[0x391907] == "test byte ptr [r15 + rax], bl"
   and Q[0x39190D] == "mov rdx, qword ptr [rsi]" and Q[0x391915] == "call 0x2fb340" and Q[0x391924] == "call 0x468a70"
   and Q[0x391952] == "add rsi, 8" and rip(0x391956, Q) == 0x2AEE0BC and Q[0x39195C] == "jl 0x391900",
   "00391710 walks ids 0 .. [02AEE0BC] - 1 only: for a set bit it takes list[id] and tests its bounds against the query shape")
pl = bytearray(d); o = off(0x3929BD); pl[o:o + 6] = bytes.fromhex("8d8ea1000000")   # lea ecx, [rsi + 0xa1]
Pp = body(bytes(pl), 0x392740, 702)
ok("C", Pp[0x3929BD] == "lea ecx, [rsi + 0xa1]" and Pp[0x3929BD] != P[0x3929BD] and byte_of(3, 288, 0x24) == byte_of(4, 0, 0x24),
   "a planted base 0xA1 is read as such; id 288 of cell 3 lands on cell 4's byte 0")
print("FAILS", fails); sys.exit(1 if fails else 0)
