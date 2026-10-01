"""G-2: who reads a SabFile sequence entry's +8 flag and +0xC float (record +0x28 / +0x2C)? (OPUS, 2026-09-27). Static.

Every caller of the SabFile accessor family 007CF500..007CFC80 (rel32 scan) is followed after each call: the returned
pointer (rax) and the out-descriptor the caller passed in rdx, through one dereference. The engine is shown live by a
positive control - it must find the entry's +4 word reads the page already cites (the walker's 007E68B0).
  E1 40 caller functions, all outside the family
  E2 POSITIVE CONTROL: word reads at +4 on the resolved entry pointer are found, 007E68B0 among them
  E3 no byte read at +8 and no dword / float read at +0xC on the same pointers, at any call site
Not claimed: an indexed walk of the entry table (base + i*16 + 8), or a copy of the record into the sound middleware -
routes this follow does not take.
"""
import re, struct, sys, bisect, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
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
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
M = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp"}
def fam(r):
    mm = re.match(r"(r\d+)[dwb]?$", r); return M.get(r, mm.group(1) if mm else r)
FAM = {f for f in sizes if 0x7CF500 <= f < 0x7CFC80}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

callers = collections.defaultdict(set)
for ch, vs, va, rs, ro in SECS:
    if not ch & 0x20000000: continue
    for p in range(ro, ro + rs - 5):
        if d[p] == 0xE8:
            v = BASE + va + p - ro; t = v + 5 + struct.unpack_from("<i", d, p + 1)[0]
            if t in FAM:
                k = bisect.bisect_right(keys, v) - 1
                if k >= 0 and v < keys[k] + sizes[keys[k]]: callers[keys[k]].add((v, t))
check("E1 the family's callers", len(callers) >= 30 and not (set(callers) & FAM), "%d functions" % len(callers))

found = collections.defaultdict(list)
for f, sites in sorted(callers.items()):
    body = list(cs.disasm(d[off(f):off(f) + sizes[f]], f)); idx = {x.address: i for i, x in enumerate(body)}
    for v, t in sorted(sites):
        i = idx.get(v)
        if i is None: continue
        pair = next((y.op_str.split(", ", 1)[1] for y in body[max(0, i - 8):i][::-1] if y.mnemonic == "lea" and y.op_str.startswith("rdx,")), None)
        ptrs = {"rax"}; derefd = set()
        for y in body[i + 1:i + 40]:
            m = re.match(r"(\w+), qword ptr (\[.+\])$", y.op_str)
            if y.mnemonic == "mov" and m and (m.group(2) == pair or any(re.fullmatch(r"\[%s\]" % r, m.group(2)) for r in ptrs)):
                derefd.add(fam(m.group(1)))
            for op in y.operands:
                if op.type == CS_OP_MEM and op.mem.base and fam(y.reg_name(op.mem.base)) in (derefd | ptrs):
                    found[(op.mem.disp, op.size)].append(y.address)
            if y.mnemonic == "call": ptrs -= {"rax"}
            if y.mnemonic == "ret": break
w4 = found.get((4, 2), [])
check("E2 positive control: the entry's +4 word reads are found (007E68B0 among them)", 0x7E68B0 in w4, "%d reads" % len(w4))
bad = found.get((8, 1), []) + found.get((0xC, 4), [])
check("E3 no byte read at +8 and no dword/float read at +0xC on the resolved pointers", not bad, str(["%08X" % a for a in bad][:6]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
