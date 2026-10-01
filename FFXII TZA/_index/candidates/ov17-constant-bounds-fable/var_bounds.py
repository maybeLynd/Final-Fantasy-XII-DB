"""var_bounds.py - OV-17 residue: are variable-descriptor operands in range? (FABLE, Claude Opus 5.5, 2026-09-29).
STATIC (image) + DATA (every shipped .ebp).

  R  THE RESOLVER ScriptVariable_Resolve 00262440 reads [table + index*8 + 4] (table = slot +0x78, the header's +0x28)
     with no compare against the table's count; its four callers are listed
  H  THE TABLE HEADER: {u32 count, count x 8-byte descriptors}; 4 + 8*count fits before the next table the header names
  C  PER OPCODE 0x48 PUSHV, 0x49 POPV, 0x4A PUSHDBG, 0x4B PUSHP: operands at or past the descriptor count. An opcode whose
     operand is not a descriptor index would show violations here instead of being assumed
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
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
        for i in range(n)]
TX = [s for s in SECS if s[0] == b".text"][0]
def off(v): return v - B - TX[2] + TX[4]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
r = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x262440):off(0x262490)], 0x262440)}
callers = [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == 0x262440]
check("R", r.get(0x262459) == "mov rax, qword ptr [rcx + 0x78]" and r.get(0x26247C) == "mov r12d, dword ptr [rax + r10*8 + 4]"
      and not any(s.startswith("cmp") for a, s in r.items() if a < 0x26247C),
      "unbounded descriptor read; callers %s" % ["%08X" % c for c in callers])
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
f = io.open(VBF, "rb"); names, blocks = V.load_index(f)
files = scripts = hdr_bad = 0
seen = collections.Counter(); over = collections.Counter(); ex = {}; last = 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try: b = V.read_entry(f, names, blocks, path)
    except Exception: continue
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    sec = b[0x80:0x80 + U32(b, 0x84)]; files += 1
    tabs = [I32(sec, k) for k in (0x20, 0x24, 0x28, 0x2C)]
    base = tabs[2]; cnt = U32(sec, base)
    nxt = min([v for v in tabs + [U32(sec, 0x18), len(sec)] if v > base], default=len(sec))
    if 4 + 8 * cnt > nxt - base: hdr_bad += 1
    diroff = U32(sec, 0x18); dc = U32(sec, diroff)
    if dc > 0x400 or diroff + 4 + dc * 0x30 > len(sec): continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(dc))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        scripts += 1
        for pc, op, imm in decode(sec[start:end]):
            if op in (0x48, 0x49, 0x4A, 0x4B):
                seen[op] += 1
                if imm >= cnt:
                    over[op] += 1; ex.setdefault(op, (path, "%x" % (start + pc), imm, cnt))
                elif imm == cnt - 1: last += 1
check("H", files > 1000 and hdr_bad == 0, "%d files; descriptor tables overrunning the next table: %d" % (files, hdr_bad))
names_ = {0x48: "PUSHV", 0x49: "POPV", 0x4A: "PUSHDBG", 0x4B: "PUSHP"}
for op in (0x48, 0x49, 0x4A, 0x4B):
    print("      %-7s operands %9d, at or past the count %d%s" % (names_[op], seen[op], over[op], ("  e.g. %s" % (ex[op],)) if op in ex else ""))
check("C", scripts > 10000 and seen[0x48] and seen[0x49] and over[0x48] == 0 and over[0x49] == 0 and over[0x4B] == 0,
      "PUSHV / POPV / PUSHP operands all below the descriptor count (PUSHDBG reported, not asserted)")
check("M", last > 0, "sensitivity: %d operands at the table's last slot" % last)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
