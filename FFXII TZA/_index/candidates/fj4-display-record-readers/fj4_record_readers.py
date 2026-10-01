"""fj4_record_readers.py - FJ-4 (FABLE, Claude Opus 5.5, 2026-09-27): interprocedural census of reads of the nine unit-display records in the menu block ([0209AC30] +0x408 + i*0xC0,
pointer list +0xAC8). Record pointers are followed through copies, stack spills, into callees receiving them in
rcx/rdx/r8/r9 (depth 3), and out of functions that return one (accessors; their callers are re-analysed)."""
import re, collections, sys
R64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", **{"r%dd" % j: "r%d" % j for j in range(8, 16)}}
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}; ARGS = ["rcx", "rdx", "r8", "r9"]
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _n = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
_secs = [struct.unpack_from("<IIII", d, _pe + 24 + _opt + i * 40 + 8) for i in range(_n)]
def off(v):
    for vs, va, rs, ro in _secs:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
SIZES = {}
for _l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    _q = _l.rstrip("\n").split("\t")
    try: SIZES[int(_q[0], 16)] = int(_q[2])
    except (ValueError, IndexError): pass
_cs = Cs(CS_ARCH_X86, CS_MODE_64)
by_f = collections.defaultdict(list)
for _f in sorted(SIZES):
    if not 0x121000 <= _f < 0x8C0000 or SIZES[_f] <= 0: continue
    _o = off(_f)
    if _o is None: continue
    for _x in _cs.disasm(d[_o:_o + SIZES[_f]], _f):
        _m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", _x.op_str)
        _t = " ; =>%08X" % (_x.address + _x.size + (int(_m.group(2), 16) if _m.group(1) == "+" else -int(_m.group(2), 16))) if _m else ""
        by_f["%08X" % _f].append(["%08X" % _x.address, "%08X" % _f, _x.mnemonic, _x.op_str + _t])
MEM = re.compile(r"(byte|word|dword|qword|xmmword) ptr \[(r\w+)(?: \+ (r\w+)(?:\*(\d))?)?(?: ([+-]) (0x[0-9a-f]+|\d+))?\]")
SLOTS = [0x408 + i * 0xC0 for i in range(9)]
hits = collections.defaultdict(set); returns_rec = set(); seen = set(); callers_of = collections.defaultdict(set)
for f, L in by_f.items():
    for a, _, mn, ops in L:
        if mn in ("call", "jmp") and ops.startswith("0x"): callers_of["%08X" % int(ops.split()[0], 16)].add(f)
def run(f, rec0, depth, via):
    key = (f, tuple(sorted(rec0)))
    if key in seen or depth < 0 or f not in by_f: return
    seen.add(key)
    H = set(); REC = set(rec0); stk = set()
    L = by_f[f]
    for k, (a, _, mn, ops) in enumerate(L):
        o = ops.split(" ;")[0]
        dst = o.split(",")[0].strip(); d64 = R64.get(dst, dst); src = o.split(",", 1)[1].strip() if "," in o else ""
        if mn == "mov" and "=>0209AC30" in ops and "qword ptr" in src: H.add(d64); REC.discard(d64); continue
        for m in MEM.finditer(o):
            w = W[m.group(1)]; r = m.group(2); idx = m.group(3); disp = int(m.group(6), 0) if m.group(6) else 0
            if m.group(5) == "-": disp = -disp
            is_dst = o.startswith(m.group(0)) and mn.startswith("mov")
            if r in REC and 0 <= disp < 0xC0 and not idx and not is_dst: hits[disp].add((f, a, w, via))
            if r in H and 0x408 <= disp < 0x408 + 9 * 0xC0 and not idx and not is_dst: hits[(disp - 0x408) % 0xC0].add((f, a, w, via + "/fixed"))
        m = re.fullmatch(r"(r\w+), qword ptr \[(r\w+)(?: \+ r\w+\*8)? \+ (0x[0-9a-f]+)\]", o)
        if mn == "mov" and m and m.group(2) in H and 0xAC8 <= int(m.group(3), 16) < 0xAC8 + 72:
            REC.add(R64.get(m.group(1), m.group(1))); continue
        m = re.fullmatch(r"(r\w+), \[(r\w+)(?: \+ r\w+)? \+ (0x[0-9a-f]+)\]", o)
        if mn == "lea" and m and m.group(2) in H and int(m.group(3), 16) in SLOTS: REC.add(R64.get(m.group(1), m.group(1))); continue
        m = re.fullmatch(r"(r\w+), (r\w+)", o)
        if mn == "mov" and m and m.group(2) in REC: REC.add(R64.get(m.group(1), m.group(1))); continue
        if mn == "mov" and m and m.group(2) in H: H.add(R64.get(m.group(1), m.group(1))); continue
        m = re.fullmatch(r"qword ptr \[rsp \+ (0x[0-9a-f]+|\d+)\], (r\w+)", o)
        if mn == "mov" and m and m.group(2) in REC: stk.add(m.group(1)); continue
        m = re.fullmatch(r"(r\w+), qword ptr \[rsp \+ (0x[0-9a-f]+|\d+)\]", o)
        if mn == "mov" and m and m.group(2) in stk: REC.add(R64.get(m.group(1), m.group(1))); continue
        if mn in ("call", "jmp") and o.startswith("0x"):
            c = "%08X" % int(o.split()[0], 16)
            passed = {r for r in ARGS if r in REC}
            if passed and c in by_f and not (mn == "jmp" and c == f): run(c, passed, depth - 1, via + ">" + c)
            if mn == "call":
                H -= VOL; REC -= VOL
                if c in returns_rec: REC.add("rax")
            continue
        if mn == "ret" and "rax" in REC: returns_rec.add(f)
        if re.fullmatch(r"r\w+|e\w\w", dst) and mn not in ("cmp", "test", "push"):
            H.discard(d64); REC.discard(d64)
fs = [f for f, L in by_f.items() if any("=>0209AC30" in x[3] for x in L)]
for rnd in range(3):
    before = len(returns_rec)
    for f in fs: run(f, set(), 3, f)
    for g in list(returns_rec):
        for c in callers_of.get(g, ()): run(c, set(), 3, c + "<" + g)
    if len(returns_rec) == before: break
    seen.clear()
print("record-returning accessors:", sorted(returns_rec))
funcs_by_off = {}
for k in sorted(hits):
    fns = sorted({x[0] for x in hits[k]})
    funcs_by_off[k] = fns
    print("+0x%02X w%s: %d reads, %d functions: %s" % (k, sorted({x[2] for x in hits[k]}), len(hits[k]), len(fns), " ".join(fns[:14])))
