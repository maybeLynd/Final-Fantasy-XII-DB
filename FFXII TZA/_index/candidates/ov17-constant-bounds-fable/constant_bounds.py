"""constant_bounds.py - OV-17, the authored-input half for script constants (FABLE, Claude Opus 5.5, 2026-09-29).
STATIC (image) + DATA (every shipped .ebp in the VBF).

  I  THE INTERPRETER does not bound PUSHI / PUSHF: PUSHI (0x4E, 00261855) reads [intPool + operand*4 + 4] and PUSHF
     (0x50, 0026187D) reads [floatPool + operand*4 + 4], with no compare. PUSHTAG (0x4C, 002617C9) IS bounded: it compares
     the operand with the tag sub-table's count (cmp eax,[rdx] / jae) and pushes 0x8000 when out of range
  H  THE POOL HEADER: each pool is {u32 count, count x 4-byte records}; checked per file by requiring
     4 + 4*count <= the distance to the next table the header names (a count that ran past it would fail H)
  C  THE CENSUS: every PUSHI / PUSHF operand in every script of every shipped .ebp is below its pool's count
  M  SENSITIVITY: operands that use their pool's last slot are counted; each would fail C against a pool one shorter
  Decoding: the linear decoder of members/gen_req_channel_census.py (3-byte ops at >= 0x48), per script region between
  directory starts. Not claimed here: jump / label targets, variable-descriptor indices (other operand kinds of OV-17).
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
lin = {x.address: ("%s %s" % (x.mnemonic, x.op_str)) for x in cs.disasm(d[off(0x25E550):off(0x261DDB)], 0x25E550)}
check("I", lin.get(0x261855) == "mov rax, qword ptr [r13 + 0x68]" and lin.get(0x26185C) == "mov edx, dword ptr [rax + rcx*4 + 4]"
      and lin.get(0x26187D) == "mov rax, qword ptr [r13 + 0x70]" and lin.get(0x261884) == "movss xmm1, dword ptr [rax + rcx*4 + 4]"
      and lin.get(0x2617EC) == "cmp eax, dword ptr [rdx]" and lin.get(0x2617EE) == "jae 0x2617f7" and lin.get(0x2617E0) == "mov ecx, 0x8000",
      "PUSHI / PUSHF unbounded natively; PUSHTAG bounded (default 0x8000)")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
I32 = lambda b, o: struct.unpack_from("<i", b, o)[0]
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
f = io.open(VBF, "rb")
names, blocks = V.load_index(f)
files = scripts = hdr_bad = 0
ops = collections.Counter(); over = []; lastslot = 0; maxratio = {0x4E: 0.0, 0x50: 0.0}
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try: b = V.read_entry(f, names, blocks, path)
    except Exception: continue
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    files += 1
    tabs = {k: I32(sec, k) for k in (0x20, 0x24, 0x28, 0x2C)}
    counts = {}
    for k, op in ((0x20, 0x4E), (0x24, 0x50)):
        base = tabs[k]; cnt = U32(sec, base)
        nxt = min([v for v in list(tabs.values()) + [U32(sec, 0x18), len(sec)] if v > base], default=len(sec))
        if 4 + 4 * cnt > nxt - base: hdr_bad += 1
        counts[op] = cnt
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        scripts += 1
        for pc, op, imm in decode(sec[start:end]):
            if op in (0x4E, 0x50):
                ops[op] += 1
                if imm >= counts[op]: over.append((path, "%x" % (start + pc), "PUSHI" if op == 0x4E else "PUSHF", imm, counts[op]))
                elif counts[op]:
                    maxratio[op] = max(maxratio[op], (imm + 1) / counts[op])
                    lastslot += imm == counts[op] - 1
check("H", files > 1000 and hdr_bad == 0, "%d .ebp files; pools whose count would overrun the next table: %d" % (files, hdr_bad))
check("C", scripts > 10000 and ops[0x4E] > 0 and ops[0x50] > 0 and not over,
      "%d scripts; PUSHI %d, PUSHF %d; operands at or past their pool count: %d %s"
      % (scripts, ops[0x4E], ops[0x50], len(over), over[:5]))
check("M", lastslot > 0, "sensitivity: %d operands use their pool's last slot, so a pool one entry shorter would fail C" % lastslot)
print("      highest operand / count: PUSHI %.3f, PUSHF %.3f (1.000 = the last slot)" % (maxratio[0x4E], maxratio[0x50]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
