"""opus_fj3_consumers.py - OPUS's independent consumer census for NAS package 4 (FJ-3), 2026-09-27. Static, shipping EXE.

Question: does anything read the display record's name pointer +0x10 (the field 00329220 blanks for a unit-owned
record)? Discriminator: a reader of +0x10..+0x17 anywhere the record is delivered would make the blank observable, and
FJ-3's residue would then not be of the intent kind.

  C1 the builder is reached only by the four wrappers' tail-jumps, and the wrappers only from the ten named callers
     (rel32 scan of every executable byte); no 8-byte absolute pointer to any of the five exists anywhere in the file
  C2 the builder's RIP-relative references outside .bss are exactly 00915A08 (400.0f) and 01CEB638 (the empty string)
  C3 frame-buffer consumers (00253C70, 00254560, 00273270, 00273880, 003C3340, 0027DE30, 003FFF70): after the call no
     instruction touches frame bytes record+0x10..+0x17
  C4 register-carried consumers: the returned or passed record pointer, followed linearly and into callees three deep,
     is never dereferenced at +0x10..+0x17 - the ten call sites, the pass-throughs 00272E10 / 00272E70, the persistent
     menu block (0209AC30 table +0xAC8 loads, functions that reference it), the battle array getters 0035BAF0 /
     0035BB20 / 002734B0, the panel object's record (002C0400 r8) and the two task handlers 0029B7D0 / 0029B810 that
     00296360 registers with the record as context (+0x48)
  C5 positive control: the same engine and seeds, asked for +0x60 and +0x24, find the known reads 00254091 / 00272EA4
     (the member index) and 0029B7E4 (the handler's +0x24) - so C4's silence is not a blind engine
Not claimed: dynamic reach (a linear taint does not follow spills or copies); the census is a negative over the
enumerated delivery paths, which C1 closes for direct calls only.
"""
import bisect, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_IMM, CS_OP_MEM, CS_OP_REG

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 32 + opt + i * 40].rstrip(b"\0").decode(),
         struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0]) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
        for i in range(n)]
def off(v):
    for nm, ch, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
keys = sorted(sizes)
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
_cache = {}
def dis(f):
    if f not in _cache: _cache[f] = list(cs.disasm(d[off(f):off(f) + sizes[f]], f))
    return _cache[f]
def owner(v):
    k = bisect.bisect_right(keys, v) - 1
    return keys[k] if k >= 0 and v < keys[k] + sizes[keys[k]] else None
def text_sites(pred):
    for nm, ch, vs, va, rs, ro in SECS:
        if ch & 0x20000000:
            for p in range(ro, ro + rs - 5):
                r = pred(BASE + va + p - ro, p)
                if r: yield r
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

BUILDER = 0x329220; WRAP = {0x31FE70, 0x320040, 0x31FEC0, 0x31FF70}
CALLERS = {0x253C70, 0x254560, 0x272E10, 0x272E70, 0x273270, 0x273880, 0x283270, 0x2BFD20, 0x35BC50, 0x3C3340}
def rel32(v, p):
    if d[p] in (0xE8, 0xE9):
        t = v + 5 + struct.unpack_from("<i", d, p + 1)[0]
        f = owner(v)
        if f and any(x.address == v for x in dis(f)): return (f, v, t, d[p])
sites = list(text_sites(lambda v, p: (lambda r: r if r and r[2] in WRAP | {BUILDER} else None)(rel32(v, p))))
to_b = {(f, op) for f, v, t, op in sites if t == BUILDER}
to_w = {f for f, v, t, op in sites if t in WRAP}
absptr = [t for t in WRAP | {BUILDER} if d.find(struct.pack("<Q", t)) >= 0]
check("C1 the builder only through the four wrappers' tail-jumps; the wrappers only from the ten callers; no absolute pointer",
      to_b == {(w, 0xE9) for w in WRAP} and to_w == CALLERS and not absptr,
      "wrapper callers %d, absolute %s" % (len(to_w), absptr))

refs = set()
for x in dis(BUILDER):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if m:
        t = x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
        o = off(t)
        if o is not None and o < len(d) and any(nm != ".bss" and BASE + va <= t < BASE + va + rs and t - BASE - va < rs
                                                for nm, ch, vs, va, rs, ro in SECS):
            refs.add(t)
check("C2 the builder's non-.bss references are 400.0f and the empty string only",
      refs == {0x915A08, 0x1CEB638} and d[off(0x1CEB638)] == 0, str(["%08X" % r for r in sorted(refs)]))

FRAME = {0x253C70: (0x25408C, 0x30), 0x254560: (0x25468C, 0x20), 0x273270: (0x2732B0, 0x20), 0x273880: (0x2738B8, 0x20),
         0x3C3340: (0x3C3444, 0x30), 0x27DE30: (0x27DE58, 0x30), 0x3FFF70: (0x3FFFBD, 0x20)}
bad = []
for f, (site, base) in FRAME.items():
    for x in dis(f):
        if x.address > site:
            for mm in re.finditer(r"\[rsp \+ 0x([0-9a-f]+)\]", x.op_str):
                if base + 0x10 <= int(mm.group(1), 16) < base + 0x18: bad.append("%08X" % x.address)
check("C3 no frame-buffer consumer touches record+0x10..+0x17 after the call", not bad, str(bad))

M = {"eax": "rax", "ax": "rax", "al": "rax", "ebx": "rbx", "bx": "rbx", "bl": "rbx", "ecx": "rcx", "cx": "rcx", "cl": "rcx",
     "edx": "rdx", "dx": "rdx", "dl": "rdx", "esi": "rsi", "si": "rsi", "sil": "rsi", "edi": "rdi", "di": "rdi",
     "dil": "rdi", "ebp": "rbp", "bp": "rbp", "bpl": "rbp"}
def fam(r):
    mm = re.match(r"(r\d+)[dwb]?$", r); return M.get(r, mm.group(1) if mm else r)
reads = []; seen = set(); PAT = r"\[%s \+ 0x1[0-7]\]"
def taint(f, i0, regs, depth):
    regs = set(regs)
    for y in dis(f)[i0:i0 + 120]:
        for r in regs:
            if re.search(PAT % r, y.op_str): reads.append("%08X %s %s" % (y.address, y.mnemonic, y.op_str))
        if y.mnemonic == "call":
            if y.operands[0].type == CS_OP_IMM:
                t = y.operands[0].imm; carried = tuple(r for r in ("rcx", "rdx", "r8", "r9") if r in regs)
                if carried and depth and t in sizes and (t, carried) not in seen:
                    seen.add((t, carried)); taint(t, 0, carried, depth - 1)
            regs -= {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
        elif y.mnemonic == "mov" and len(y.operands) == 2 and y.operands[0].type == CS_OP_REG and y.operands[1].type == CS_OP_REG:
            s, t = fam(y.reg_name(y.operands[1].reg)), fam(y.reg_name(y.operands[0].reg))
            if s in regs: regs.add(t)
            else: regs.discard(t)
        elif y.operands and y.operands[0].type == CS_OP_REG and y.mnemonic not in ("cmp", "test", "push"):
            regs.discard(fam(y.reg_name(y.operands[0].reg)))
        if not regs or y.mnemonic == "ret": break
def at(f, a): return next(i for i, x in enumerate(dis(f)) if x.address == a) + 1
gf = set()
def census():
    # the ten sites: the returned pointer and the register that carried the record
    for f, v, t, op in sites:
        if t in WRAP:
            i = at(f, v); pre = [x for x in dis(f)[:i - 1] if x.op_str.startswith("r8,")]
            src = pre[-1].op_str.split(", ")[1] if pre else ""
            taint(f, i, {"rax"} | ({fam(src)} if re.match(r"^[a-z0-9]+$", src) else set()), 3)
    # pass-throughs: their callers' frames are C3 (0027DE30, 003FFF70); 00272E70's buffer is 002BFD20's object
    taint(0x272E10, 0, {"r8"}, 3); taint(0x272E70, 0, {"rcx"}, 3)
    # the persistent menu block: pointer-table loads in every function referencing 0209AC30
    global gf
    G = 0x209AC30
    gf = set(text_sites(lambda v, p: owner(v) if v + 4 + struct.unpack_from("<i", d, p)[0] == G else None)) - {None}
    for f in gf:
        for i, x in enumerate(dis(f)):
            if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[0].type == CS_OP_REG and x.operands[1].type == CS_OP_MEM:
                mem = x.operands[1].mem
                if (mem.disp == 0xAC8 and mem.index) or (mem.disp in range(0xAC8, 0xB10, 8) and not mem.index):
                    taint(f, i + 1, {fam(x.reg_name(x.operands[0].reg))}, 3)
    # the battle array getters (0035BC50's records) and the wrapper that tail-jumps one
    for f, v, t, op in text_sites(lambda v, p: (lambda r: r if r and r[2] in (0x35BAF0, 0x35BB20, 0x2734B0) and r[3] == 0xE8 else None)(rel32(v, p))):
        taint(f, at(f, v), {"rax"}, 3)
    # the panel object's record: 002C0400 (r8) and the two task handlers (context +0x48)
    taint(0x2C0400, 0, {"r8"}, 3)
    for h in (0x29B7D0, 0x29B810):
        i, x = next((i, x) for i, x in enumerate(dis(h)) if "[rcx + 0x48]" in x.op_str)
        taint(h, i + 1, {fam(x.op_str.split(",")[0])}, 3)
census()
check("C4 no register-carried record pointer is dereferenced at +0x10..+0x17 (%d menu-block functions, %d callees followed)"
      % (len(gf), len(seen)), not reads, str(reads[:6]))
neg = reads; reads = []; seen = set(); PAT = r"\[%s \+ 0x(?:60|24)\]"; census()
hit = {r.split()[0] for r in reads}
check("C5 positive control: the engine finds the known +0x60 / +0x24 reads", {"00254091", "00272EA4", "0029B7E4"} <= hit,
      "%d reads found" % len(reads))
print("FAILS", fails)
sys.exit(1 if fails else 0)
