"""jump_bounds.py - OV-17 residue: are jump operands and jump-table targets in range? (FABLE, Claude Opus 5.5, 2026-09-29).
STATIC (image) + DATA (every shipped .ebp).

  J  THE LOOKUP 003589E0 (the JMP family's shared resolver) IS bounded: an index at or past the table's count returns 0,
     i.e. the script's start
  T  EVERY JUMP TABLE (directory entry +0x14 -> {u32 count; u32 offset[count]}) fits inside its section, and no offset is
     past its script's end. An entry exactly AT the end (a label after the script's final JMP) exists in 31,235 scripts and
     is never a jump target (a first version counted these as out of range; they are the trailing label, unreachable)
  C  EVERY JUMP OPERAND (0x51 JMP .. 0x57 JMPYC) of every script is below its table's count
  M  SENSITIVITY: operands at the table's last slot
"""
import collections, hashlib, io, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "agent_flow", "tools"))
import vbfextract as V
EXE = os.path.join(ROOT, "Database", "Tools", "work", "exe", "FFXII_TZA.exe")
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
j = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x3589E0):off(0x3589F5)], 0x3589E0)}
check("J", j.get(0x3589E0) == "mov r8, qword ptr [rcx + 0x50]" and j.get(0x3589E4) == "cmp edx, dword ptr [r8]"
      and j.get(0x3589E7) == "jb 0x3589ec" and j.get(0x3589E9) == "xor eax, eax" and j.get(0x3589EF) == "mov eax, dword ptr [r8 + rax*4 + 4]",
      "jump index bounded; out of range -> offset 0")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
def decode(code):
    ins, i = [], 0
    while i < len(code):
        op = code[i]
        if op > 0x63: break
        if op >= 0x48:
            if i + 2 >= len(code): break
            ins.append((i, op, code[i + 1] | (code[i + 2] << 8))); i += 3
        else:
            ins.append((i, op, None)); i += 1
    return ins
f = io.open(VBF, "rb"); names, blocks = V.load_index(f)
files = scripts = tables = bad_tab = bad_off = end_entries = end_targeted = 0
jumps = over = last = 0; ex = []
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try: b = V.read_entry(f, names, blocks, path)
    except Exception: continue
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    sec = b[0x80:0x80 + U32(b, 0x84)]; files += 1
    diroff = U32(sec, 0x18); dc = U32(sec, diroff)
    if dc > 0x400 or diroff + 4 + dc * 0x30 > len(sec): continue
    ents = [(U32(sec, diroff + 4 + s * 0x30 + 8), U32(sec, diroff + 4 + s * 0x30 + 0x14)) for s in range(dc)]
    starts = sorted(e[0] for e in ents)
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start, lo in ents:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        scripts += 1
        if lo + 4 > len(sec): bad_tab += 1; continue
        cnt = U32(sec, lo); tables += 1
        if lo + 4 + 4 * cnt > len(sec): bad_tab += 1; continue
        offs = [U32(sec, lo + 4 + 4 * k) for k in range(cnt)]
        bad_off += sum(1 for o in offs if o > end - start)
        endidx = {k for k, o in enumerate(offs) if o == end - start}
        end_entries += len(endidx)
        for pc, op, imm in decode(sec[start:end]):
            if 0x51 <= op <= 0x57:
                jumps += 1
                if imm in endidx: end_targeted += 1
                if imm >= cnt:
                    over += 1
                    if len(ex) < 5: ex.append((path, "%x" % (start + pc), op, imm, cnt))
                elif imm == cnt - 1: last += 1
check("T", files > 1000 and tables > 10000 and bad_tab == 0 and bad_off == 0 and end_targeted == 0,
      "%d files, %d jump tables; tables past the section: %d; offsets past the script's end: %d; entries AT the end: %d, targeted by a jump: %d"
      % (files, tables, bad_tab, bad_off, end_entries, end_targeted))
check("C", jumps > 0 and over == 0, "%d jump operands; at or past the table count: %d %s" % (jumps, over, ex))
check("M", last > 0, "sensitivity: %d jump operands at the table's last slot" % last)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
