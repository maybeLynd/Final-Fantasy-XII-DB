"""BI-11: handle classes 5/6/9 of the PackedIdBucketRegistry are the presentation-record classes (OPUS, 2026-09-27).

  C1 the only creator: 003B02A0 admits a class only when (class-5) & ~5 == 0 and class != 10, i.e. {5, 6, 9}
     (003B02D7-003B02EA), mints the handle `class << 28 | ++serial` (003B03BB-003B03E4) and writes the class as the
     record's byte 0 (003B03D7); its 0x3B0-byte record is zeroed first (003B03A8-003B03B6).
  C2 the cap: an unflagged presentation number is refused when 002FC9B0() + 003B0B70() >= 24 (003B0377-003B0388);
     the per-id byte table is 01EFE260 (003B0321-003B032F).
  C3 the census of every direct call to 003B02A0 and its class argument ([rsp+0x20]):
       002EACD0 5 (the level-up / attached-effect spawner), 0036E700 5, 003A3E30 5, 003B0C30 5 (from
       CharacterRenderRecord_UpdateRootAnimationPresentationPhase 0042C410, number 0x63), 003B0C50 5 (the footstep
       effect), 003BA1F0 9, and 0036E750 passing its own 5th argument through. 0036E750's callers pass 9 (002EFD80,
       002EFDC0, 003B7180) or a register (00357620, the script bridge). No direct call passes a constant 6.
  C4 0036E750 maps its index through the u32 table 01EF9400 (0036E75D-0036E76B) before the call.
  C5 class 1: 002FC200 initialises the 48 x 0x38 records at 02EC32E0 with dword +0 = (1 << 28) + slot
     (and ecx, 0x3f / bts ecx, 0x1c, loop to 0x30).
  C6 its loader 002FC4A0 sums the 5-bit cost word[02EC19C4 + id*8] over live records in states 5-7, adds the new
     record's own (id = word +0x20), refuses above 24 (cmp eax, 0x18 / jg), and requests resource kind 0x26, or 0x0B
     when 002DEBB0() is non-zero, for that id through 002DF980.
  C7 002FCFF0 fills the 512 sizes of that table from 0032E400 with the same kind choice (0x26 / 0x0B), so the
     table and the loads are the file-size-table kinds 38 / 11 - effect_finish/*/magic/*.efx (fst page).
  C8 the shared budget: 003B02A0 adds 002FC9B0 (the same class-1 cost sum) to 003B0B70 before its 24 cap.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]


def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True


def ins(a, size):
    return list(cs.disasm(d[off(a):off(a) + size], a))


def txt(a, size):
    return "\n".join("%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in ins(a, size))


fails = 0


def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)


t = txt(0x003B02A0, 0x1D0)
check("C1a the class gate admits exactly {5,6,9}",
      "003B02D7 lea eax, [r13 - 5]" in t and "003B02DB test eax, 0xfffffffa" in t and "003B02E6 cmp r13d, 0xa" in t
      and sorted(c for c in range(16) if ((c - 5) & 0xFFFFFFFA) == 0 and c != 10) == [5, 6, 9])
check("C1b handle = class << 28 | serial; class is record byte 0; 0x3B0 record cleared",
      "003B03C6 shl eax, 0x1c" in t and "003B03CF and ecx, 0xfffffff" in t and "003B03D7 mov byte ptr [rsp + 0x8c0], r13b" in t
      and "003B03B0 mov r8d, 0x3b0" in t)
x = [i for i in ins(0x003B0321, 8)][0]
check("C2 the 24 cap and the 01EFE260 per-id table",
      "003B0385 cmp eax, 0x18" in t and x.address + x.size + x.operands[1].value.mem.disp == 0x01EFE260)

funcs = []
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    c = line.split("\t")
    try:
        funcs.append((int(c[0], 16), int(c[2])))
    except (ValueError, IndexError):
        continue


def class_args(target):
    out = {}
    for e, sz in funcs:
        if not 0 < sz <= 0x20000 or off(e) is None:
            continue
        body = list(cs.disasm(d[off(e):off(e) + sz], e))
        for k, i in enumerate(body):
            if i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM and i.operands[0].imm == target:
                v = "?"
                for j in range(k - 1, max(-1, k - 12), -1):
                    p = body[j]
                    if p.mnemonic == "call" or p.mnemonic.startswith("j"):
                        break
                    if p.mnemonic == "mov" and p.operands[0].type == X86_OP_MEM and p.operands[0].value.mem.disp == 0x20 \
                            and p.reg_name(p.operands[0].value.mem.base) == "rsp":
                        v = p.operands[1].imm if p.operands[1].type == X86_OP_IMM else "reg"
                        break
                out.setdefault(e, []).append(v)
    return out


a = class_args(0x003B02A0)
want = {0x002EACD0: [5], 0x0036E700: [5], 0x003A3E30: [5], 0x003B0C30: [5], 0x003B0C50: [5], 0x0036E750: ["reg"], 0x003BA1F0: [9]}
check("C3a every direct caller of 003B02A0 and its class", a == want, str({("%08X" % k): v for k, v in a.items()}))
b = class_args(0x0036E750)
wantb = {0x002EFD80: [9], 0x002EFDC0: [9], 0x003B7180: [9], 0x00357620: ["reg"]}
check("C3b 0036E750's callers pass 9 or the script bridge's register; no constant 6 anywhere",
      b == wantb and all(6 not in v for v in list(a.values()) + list(b.values())), str({("%08X" % k): v for k, v in b.items()}))
y = ins(0x0036E75D, 8)[0]
check("C4 0036E750 maps its index through 01EF9400", y.address + y.size + y.operands[1].value.mem.disp == 0x01EF9400)
t5 = txt(0x002FC200, 0x90)
check("C5 002FC200: 48 class-1 records, dword +0 = (1<<28) + slot",
      "002FC257 and ecx, 0x3f" in t5 and "002FC25A bts ecx, 0x1c" in t5 and "002FC286 cmp r8d, 0x30" in t5)
t6 = txt(0x002FC4A0, 0x100)
check("C6 002FC4A0: cost sum over states 5-7 plus own cost, refuse above 24, request kind 0x26/0x0B by id +0x20",
      "002FC4E7 lea ecx, [rdx - 5]" in t6 and "002FC4EA cmp cl, 2" in t6 and "002FC508 movzx ebx, word ptr [r15 + 0x20]" in t6
      and "002FC519 cmp eax, 0x18" in t6 and "002FC585 mov edx, 0x26" in t6 and "002FC58C mov ecx, 0xb" in t6
      and "002FC599 call 0x2df980" in t6)
t7 = txt(0x002FCFF0, 103)
check("C7 002FCFF0: the 512 table sizes from 0032E400 with kind 0x26 / 0x0B",
      "002FD00D mov esi, 0x200" in t7 and "002FD012 lea ebp, [rbx + 0x26]" in t7 and "002FD01C mov ecx, 0xb" in t7
      and "002FD027 call 0x32e400" in t7)
check("C8 the shared 24 budget: 003B02A0 adds 002FC9B0 to 003B0B70",
      "003B0377 call 0x2fc9b0" in t and "003B037E call 0x3b0b70" in t and "003B0383 add eax, ebx" in t)
print("FAILS", fails)
sys.exit(1 if fails else 0)
