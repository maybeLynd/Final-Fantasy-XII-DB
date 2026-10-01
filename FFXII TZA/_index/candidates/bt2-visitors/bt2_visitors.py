"""BT-2: the record-tree iterator's visitors run, and the +0x3D4 name (OPUS, 2026-09-27). Control. Static.

CharacterRenderRecord (0x740 per record at [022C6F28]). The row's last named route was the iterator 0042EF90(index,
visitor, arg): a child (+8) / sibling (+0xA) walk calling visitor(record, arg), with the visitor passed through (97 call
sites, none loading it locally), plus three RIP-slot calls.
  V1 the visitor resolved at the call sites: rdx traced back, through parameters, up to three caller levels - 43
     distinct visitors; at most three sites stay unresolved (indirect call rbp / rsi)
  V2 POSITIVE CONTROL: the visitors, followed with their helpers two deep, reach named rows of the record
  V3 no visitor route touches any byte of a DISCOVERED row
  V4 the three RIP-slot calls are CRT imports - strstr (slot 008C2A08, twice) and strncpy (008C2F70) - and the only
     strncpy wrapper, 00409210 (a 32-byte name copy), is called with no render record as its destination
     (00409780: a global buffer; 0041D220: presentation entry +0x2EC; 00424D80: a stack buffer)
  V5 +0x3D4 is a NUL-terminated name, not a byte: 0042F7DD takes its address and 004218A0 hands it to 00372760, an
     inlined strcmp over the element table's 0x4C-byte entries (0037279A lea r10, [rax+0x30]; 003727B0-003727C1 the
     byte loop through the string pointer; 003727CA add r10, 0x4c), returning the matching index; the next field is
     +0x3F4, so the name is char[32] and the DISCOVERED span +0x3D5..+0x3F3 is its tail, read through the pointer
Not claimed: the name's writer; what the other DISCOVERED spans hold.
"""
import re, struct, sys, bisect, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_REG, CS_OP_MEM, CS_OP_IMM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
_c = {}
def D(f):
    if f not in _c: _c[f] = list(cs.disasm(d[off(f):off(f) + sizes.get(f, 0x300)], f))
    return _c[f]
def rip(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16) if m else None
M = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
def fam(r):
    mm = re.match(r"(r\d+)[dwb]?$", r); return M.get(r, mm.group(1) if mm else r)
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

calls = collections.defaultdict(list)
for ch, vs, va, rs, ro in SECS:
    if ch & 0x20000000:
        for p in range(ro, ro + rs - 5):
            if d[p] in (0xE8, 0xE9):
                v = BASE + va + p - ro; t = v + 5 + struct.unpack_from("<i", d, p + 1)[0]
                if t in sizes:
                    f = owner(v)
                    if f: calls[t].append((f, v))
def resolve(f, site, reg, depth, trail):
    b = D(f); i = next((k for k, x in enumerate(b) if x.address == site), None)
    if i is None: return [("unknown", None)]
    cur = reg
    for x in b[:i][::-1]:
        ops = [o.strip() for o in x.op_str.split(",")]
        if not ops or fam(ops[0]) != cur: continue
        if x.mnemonic == "lea" and rip(x): return [("fn", rip(x))]
        if x.mnemonic == "mov" and len(ops) == 2 and re.fullmatch(r"\w+", ops[1]): cur = fam(ops[1]); continue
        return [("unknown", None)]
    if cur in ("rcx", "rdx", "r8", "r9") and depth > 0:
        out = []
        for g, s in calls.get(f, [])[:40]:
            if (g, s) not in trail: out += resolve(g, s, cur, depth - 1, trail | {(g, s)})
        return out or [("unknown", None)]
    return [("unknown", None)]
vis = collections.Counter(); unresolved = 0
for f, s in calls[0x42EF90]:
    if f == 0x42EF90: continue
    r = resolve(f, s, "rdx", 3, frozenset())
    got = [v for k, v in r if k == "fn"]
    for v in got: vis[v] += 1
    unresolved += (not got)
check("V1 visitors resolved at the iterator's call sites", len(calls[0x42EF90]) >= 90 and len(vis) >= 40 and unresolved <= 3,
      "%d sites, %d visitors, %d unresolved" % (len(calls[0x42EF90]), len(vis), unresolved))

acc = collections.defaultdict(set); seen = set()
def follow(f, regs, depth):
    regs = set(regs)
    for y in D(f)[:300]:
        for op in y.operands:
            if op.type == CS_OP_MEM and op.mem.base and y.mnemonic != "lea" and fam(y.reg_name(op.mem.base)) in regs and op.mem.index == 0 and 0 <= op.mem.disp < 0x740:
                for k in range(op.mem.disp, op.mem.disp + max(op.size, 1)): acc[k].add(y.address)
        if y.mnemonic in ("call", "jmp") and y.operands and y.operands[0].type == CS_OP_IMM:
            t = y.operands[0].imm; carried = tuple(r for r in ("rcx", "rdx", "r8", "r9") if r in regs)
            if carried and depth and t in sizes and (t, carried) not in seen:
                seen.add((t, carried)); follow(t, carried, depth - 1)
            if y.mnemonic == "jmp": break
            regs -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}; continue
        if y.mnemonic == "mov" and len(y.operands) == 2 and y.operands[0].type == CS_OP_REG and y.operands[1].type == CS_OP_REG:
            s, t = fam(y.reg_name(y.operands[1].reg)), fam(y.reg_name(y.operands[0].reg))
            if s in regs: regs.add(t)
            else: regs.discard(t)
        elif y.operands and y.operands[0].type == CS_OP_REG and y.mnemonic not in ("cmp", "test", "push"):
            regs.discard(fam(y.reg_name(y.operands[0].reg)))
        if not regs or y.mnemonic == "ret": break
for v in vis: follow(v, {"rcx"}, 2)
rows = []
for l in open(DB / "_types" / "fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if c[0] == "CharacterRenderRecord" and len(c) > 6:
        rows.append((int(c[1], 16), int(c[2]), c[3], c[6]))
named_hit = [r for r in rows if r[3] != "DISCOVERED" and any(k in acc for k in range(r[0], r[0] + r[1]))]
disc_hit = [r for r in rows if r[3] == "DISCOVERED" and any(k in acc for k in range(r[0], r[0] + r[1]))]
check("V2 positive control: the visitor routes reach named rows", len(named_hit) >= 20, "%d named rows" % len(named_hit))
check("V3 no visitor route touches a DISCOVERED row", not disc_hit, str([(hex(r[0]), r[2]) for r in disc_hit][:4]))

def cstr(v): return d[off(v):off(v) + 32].split(b"\0")[0]
def import_name(slot):
    o = off(BASE + struct.unpack_from("<Q", d, off(slot))[0]); return d[o + 2:o + 32].split(b"\0")[0]
x1 = next(x for x in D(owner(0x1ED0FC)) if x.address == 0x1ED0FC)
x2 = next(x for x in D(owner(0x1EDD88)) if x.address == 0x1EDD88)
x3 = next(x for x in D(owner(0x40922E)) if x.address == 0x40922E)
dests = []
for f, s in calls[0x409210]:
    b = D(f); i = next(k for k, x in enumerate(b) if x.address == s)
    rc = next((y for y in b[max(0, i - 8):i][::-1] if y.op_str.startswith("rcx,")), None)
    dests.append("%s %s" % (rc.mnemonic, rc.op_str) if rc else "?")
check("V4 the RIP-slot calls are strstr / strncpy imports; the 32-byte name copy 00409210 never targets a render record",
      rip(x1) == rip(x2) == 0x8C2A08 and import_name(0x8C2A08) == b"strstr" and rip(x3) == 0x8C2F70 and import_name(0x8C2F70) == b"strncpy"
      and sorted(dests) == sorted(["mov rcx, rdi", "add rcx, 0x2ec", "lea rcx, [rsp + 0x70]"]), str(dests))

A = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x42F6C0)}
S = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x372760)}
N = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in D(0x4218A0)}
nextrow = min(r[0] for r in rows if r[0] > 0x3D4 and r[3] != "DISCOVERED")
check("V5 +0x3D4 is a char[32] name: address taken, strcmp'd against the element table's 0x4C-byte entries; next field +0x3F4",
      A.get(0x42F7DD) == "lea rdx, [rsi + 0x3d4]" and A.get(0x42F7E7) == "call 0x4218a0"
      and N.get(0x4218C1) == "mov r12, rdx" and N.get(0x421966) == "mov rdx, r12" and N.get(0x42196C) == "call 0x372760"
      and S.get(0x37279A) == "lea r10, [rax + 0x30]" and S.get(0x3727B0) == "movzx edx, byte ptr [rax]"
      and S.get(0x3727B3) == "movzx ecx, byte ptr [rax + r8]" and S.get(0x3727CA) == "add r10, 0x4c"
      and nextrow == 0x3F4, "next named row +0x%X" % nextrow)
print("FAILS", fails)
sys.exit(1 if fails else 0)
