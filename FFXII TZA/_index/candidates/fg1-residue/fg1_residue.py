"""fg1_residue.py - FG-1's three remaining sub-questions, each settled from bytes and shipped data (OPUS, 2026-09-27).

  R1 the rank table's +4 count (00315390 takes 00316480()'s result as r8 and compares it with the row's +4 byte).
     00316480 walks the menuhandbook.bin 'hcom' blob bound at [022C2550]: p = blob+8, p += u16[p], p += u16[p], then
     u16 count at +2 and 2-byte entries {u8 questId, u8 minimum} from +4. An entry counts when quest-registry bit
     +0x1020 (0046B1A0, verb 0x1D0 isquestclear) or +0x1000 (0046B240, 0x1CF isquestorder) is set AND the quest
     scenario flag +0x1064[id] (0046B180, verb 0x2B4 getquestscenarioflag) is >= the minimum (setge). Shipped node:
     45 entries, ids 128..172 each exactly once, minima in {30, 50, 70, 90, 100}, identical in all nine locales.
  R2 +0x334C (256 bits) and +0x336C (256 nibbles) of the image-backed block. Image-wide, the only instructions with a
     displacement in either range are 00315620 / 00315470 (read) and 00315A20 / 00315CD0 (write); the writers' only
     caller is 00577A40 (the hdat entry op-program executor) and the readers' are 00575E80 (the hchk gate) and
     00577A40. Shipped data exercises neither side: every non-monster hchk record (2,844) holds the 0xFF sentinel in
     both the nibble-selector and the bit slot, and every hdat string entry's op count is 0.
  R3 +0x30 u16[32] / +0x70 u8[32] / +0x90 u32[101] (classes 6/7/8) are the remembered menu cursor positions:
     the Cursor Position setter 002DE1E0 writes option bit 15 and tail-jumps 002526D0, which memsets block+0x30 for
     0x1F4 bytes through the slot 020927C0; the reader 002526F0 first calls 002DDD50, the option's bit-15 getter.
Mutants: M1 one hchk selector planted to 5 is counted; M2 one hdat op count planted to 1 is counted.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import glob, os, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

ROOT = Path(__file__).resolve().parents[5]
EXTRACT = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
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


def text(a, size):
    return ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in ins(a, size)]


fails = 0


def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)


# R1 -------------------------------------------------------------------------------------------------------------
t = text(0x00316480, 289)
body = "\n".join(t)
x = ins(0x00316490, 8)[0]
check("R1a 00316480 loads the blob pointer from [022C2550]",
      x.address + x.size + x.operands[1].value.mem.disp == 0x022C2550)
check("R1b the walk: p = blob+8, two u16 self-relative hops, count at +2, entry id at +4 and minimum at +5",
      all(s in body for s in ("lea rcx, [rdx + 8]", "movzx eax, word ptr [rcx]", "cmp ax, word ptr [rcx + 2]",
                               "movzx ecx, byte ptr [rcx + rax*2 + 4]", "movzx ecx, byte ptr [rbx + 5]", "setge r8b")))
check("R1c the three tests: 0046B1A0 or 0046B240, then 0046B180 >= minimum",
      all(s in body for s in ("call 0x46b1a0", "call 0x46b240", "call 0x46b180")))
check("R1d 0046B1A0 tests +0x1020, 0046B240 tests +0x1000, 0046B180 reads byte +0x1064",
      any("[rax + rdi + 0x1020]" in s for s in text(0x0046B1A0, 72))
      and any("[rax + rdi + 0x1000]" in s for s in text(0x0046B240, 72))
      and any("[rax + rbx + 0x1064]" in s for s in text(0x0046B180, 28)))
check("R1e 00315390 feeds 00316480's result to the +4 comparison",
      "call 0x316480" in "\n".join(text(0x00315390, 94)) and "movzx edx, byte ptr [rcx - 1]" in "\n".join(text(0x00315390, 94)))
nodes = {}
for f in sorted(glob.glob(os.path.join(EXTRACT, "*", "handbook", "menuhandbook.bin"))):
    b = open(f, "rb").read()
    p = 8; p += struct.unpack_from("<H", b, p)[0]; p += struct.unpack_from("<H", b, p)[0]
    cnt = struct.unpack_from("<H", b, p + 2)[0]
    nodes[f] = tuple(tuple(b[p + 4 + 2 * i:p + 6 + 2 * i]) for i in range(cnt))
vals = set(nodes.values())
ent = next(iter(vals)) if len(vals) == 1 else ()
check("R1f the shipped node: 45 entries, ids 128..172 once each, minima {30,50,70,90,100}, one node in all locales",
      len(nodes) == 9 and len(vals) == 1 and len(ent) == 45 and sorted(e[0] for e in ent) == list(range(128, 173))
      and {e[1] for e in ent} == {30, 50, 70, 90, 100}, "(%d locales)" % len(nodes))

# R2 -------------------------------------------------------------------------------------------------------------
funcs = []
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    c = line.split("\t")
    try:
        funcs.append((int(c[0], 16), int(c[2])))
    except (ValueError, IndexError):
        continue
hits = {}
for e, sz in funcs:
    if not 0 < sz <= 0x20000 or off(e) is None:
        continue
    for x in cs.disasm(d[off(e):off(e) + sz], e):
        for o in x.operands:
            if o.type == X86_OP_MEM and o.value.mem.base != X86_REG_RIP:
                dd = o.value.mem.disp
                if 0x334C <= dd < 0x33EC or 0xB34C <= dd < 0xB3EC or 0xB54C <= dd < 0xB5EC:   # 32 B bits + 128 B nibbles
                    hits.setdefault(e, []).append(x.address)
check("R2a image-wide, the +0x334C/+0x336C displacements sit in exactly four functions",
      sorted(hits) == [0x00315470, 0x00315620, 0x00315A20, 0x00315CD0], " ".join("%08X" % k for k in sorted(hits)))


def callers(t):
    out = set()
    for e, sz in funcs:
        if not 0 < sz <= 0x20000 or off(e) is None:
            continue
        for x in cs.disasm(d[off(e):off(e) + sz], e):
            if x.mnemonic in ("call", "jmp") and x.op_str == hex(t):
                out.add(e)
    return out


cw = callers(0x00315A20) | callers(0x00315CD0); cr = callers(0x00315470) | callers(0x00315620)
check("R2b writers called only by 00577A40; readers by 00575E80 and 00577A40",
      cw == {0x00577A40} and cr == {0x00575E80, 0x00577A40})


def hchk_census(files, plant=False):
    used = total = mins = 0
    for f in files:
        b = bytearray(open(f, "rb").read())
        if b[:4] != b"hchk" or "monster" in os.path.basename(f):
            continue
        if plant:
            b[0xC] = 5; plant = False
        for i in range(struct.unpack_from("<H", b, 8)[0]):
            r = b[0xC + 8 * i:0x14 + 8 * i]; total += 1
            used += (r[0] != 0xFF) + (r[2] != 0xFF)
            mins += struct.unpack_from("<H", r, 6)[0] != 0xFFFF
    return total, used, mins


hf = sorted(glob.glob(os.path.join(EXTRACT, "*", "handbook", "menuhandbook_*.dat")))
hchk = [f for f in hf if not os.path.basename(f)[:-4][-3:].isdigit()]
total, used, mins = hchk_census(hchk)
check("R2c every shipped non-monster hchk gate leaves both slots at 0xFF (sensitivity: the story-flag slot is used)",
      total == 2844 and used == 0 and mins > 0, "(%d records, %d slots used, %d story minima)" % (total, used, mins))
check("M1 a planted selector is counted", hchk_census(hchk, plant=True)[1] == 1)


def hdat_ops(files, plant=False):
    entries = ops = 0
    for f in files:
        b = bytearray(open(f, "rb").read())
        if b[:4] != b"hdat":
            continue
        cnt = struct.unpack_from("<H", b, 0xA)[0]; so = struct.unpack_from("<H", b, 0x10)[0]
        for i in range(cnt):
            ro = struct.unpack_from("<H", b, 0x12 + 2 * i)[0]
            for k in range(b[ro]):
                ep = so + struct.unpack_from("<I", b, ro + 4 + 4 * k)[0]
                if plant:
                    b[ep + 2] = 1; plant = False
                entries += 1; ops += b[ep + 2]
    return entries, ops


hdat = [f for f in hf if os.path.basename(f)[:-4][-3:].isdigit()]
en, op = hdat_ops(hdat)
check("R2d every shipped hdat entry's op-program count is 0", en == 12168 and op == 0, "(%d entries)" % en)
check("M2 a planted op count is counted", hdat_ops(hdat, plant=True)[1] == 1)

# R3 -------------------------------------------------------------------------------------------------------------
s1 = text(0x002DE1E0, 26); s2 = text(0x002526D0, 24); s3 = text(0x002526F0, 40); s4 = text(0x002DDD50, 16)
check("R3a the Cursor Position setter writes bit 15 and tail-jumps the table clear",
      any("shl ecx, 0xf" in s for s in s1) and any("jmp 0x2526d0" in s for s in s1))
x = ins(0x002526D0, 8)[0]
check("R3b 002526D0 clears block+0x30 for 0x1F4 bytes through the slot 020927C0",
      x.address + x.size + x.operands[1].value.mem.disp == 0x020927C0
      and any("add rcx, 0x30" in s for s in s2) and any("mov r8d, 0x1f4" in s for s in s2))
check("R3c the reader 002526F0 calls the option's bit-15 getter 002DDD50",
      any("call 0x2ddd50" in s for s in s3) and any("shr eax, 0xf" in s for s in s4))
print("FAILS", fails)
sys.exit(1 if fails else 0)
