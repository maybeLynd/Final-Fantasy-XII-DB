"""uq332_no_reader.py - UQ-332: who reads section 12's stored pointer and walks its entries? (FABLE, Claude Opus 5.5,
2026-09-27). Static. Closes the three routes the 2026-09-14 census left open; the census itself (only two accesses to
managerRecord[+0x100], both writes) is Tools/work/FABLE/regprose/mgr_field_census.py and is not re-run here.

  R1 the container route: image-wide, the only reads of an EBP container's section-12 directory slot - a dword load of
     [r + 0x40] within twelve instructions of a count test [r + 4] on the same base - are the two in the loader
     003304A0: 003304E4 tests presence and sets the pending bit 9 (003304F0 bts rcx, 9), and 003305EA feeds the
     handler 0032FB70. No function indexes the directory generically ([rA + rB*4 + 0x10] beside a [rA + 4] test).
  R2 the escapes: the four table-dispatched stores the census could not follow are the begin callbacks of the sync
     verbs entrysync (015D, 0034AF50), eventstartsync (0165, 0034F3C0) and its variants 0166 (0034E460) / 0167 (0034FC50),
     writing {manager record, index} into the verb's wait state. Their polls (0034B350, 0034F6F0, 0034EAB0) read the
     manager's byte +0x10 and no other manager field, and the only callees they hand the record to (00358940,
     00265380, 003DBF60) contain no +0x100 access in their whole callee closure.
  R3 the inversion: an entry is a packed model id ((letter << 16) | id, UQ-333), and the engine's model-id decoder is
     002ED6F0. None of its direct callers takes the id from a count-prefixed list: each loads it from an entity's
     +0x14, from its own argument, or composes it from the static letter table at 00D0F870. And the image has no
     model-name format string (the only %c%d is a soft-particle CSV line).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(W / "graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: SIZES[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a): return list(cs.disasm(d[off(a):off(a) + SIZES[a]], a))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

fixed = []; generic = []
for f, sz in sorted(SIZES.items()):
    o = off(f)
    if o is None or sz <= 0 or not (0x121000 <= f < 0x880000): continue
    ins = list(cs.disasm(d[o:o + sz], f))
    for k, x in enumerate(ins):
        m = re.match(r"dword ptr \[(r\w+) \+ 4\], ", x.op_str) if x.mnemonic == "cmp" else None
        if m:
            b = m.group(1)
            for y in ins[k + 1:k + 12]:
                if y.mnemonic == "mov" and re.search(r"dword ptr \[%s \+ 0x40\]$" % b, y.op_str):
                    fixed.append((y.address, f)); break
        g2 = re.search(r"dword ptr \[(r\w+) \+ (r\w+)\*4 \+ 0x10\]", x.op_str)
        if g2 and any(re.search(r"dword ptr \[%s \+ 4\]" % g2.group(1), y.op_str) for y in ins[max(0, k - 12):k + 4]):
            generic.append((x.address, f))
L = dis(0x3304DE, 0x3304F9)
check("R1 the only section-12 directory reads are the loader's presence test (pending bit 9) and its handler dispatch; no generic accessor",
      sorted(fixed) == [(0x3304E4, 0x3304A0), (0x3305EA, 0x3304A0)] and generic == []
      and L.get(0x3304DE) == "cmp dword ptr [rdi + 4], 0xc" and L.get(0x3304F0) == "bts rcx, 9"
      and dis(0x3305F8, 0x3305FF).get(0x3305FA) == "call 0x32fb70", "fixed %s generic %d" % (["%08X" % a for a, _ in fixed], len(generic)))

esc = {0x34E4B3: 0x34E460, 0x34F41D: 0x34F3C0, 0x34FCB7: 0x34FC50, 0x34AF69: 0x34AF50}
esc_ok = all(dis(s, s + 4).get(s, "").startswith("mov qword ptr [r") and "], rax" in dis(s, s + 4).get(s, "") for s in esc)
polls = [0x34B350, 0x34F6F0, 0x34EAB0]
mgr_reads = set()
for p in polls:
    ins = body(p)
    mregs = set()
    for x in ins:
        if re.match(r"r\w+, qword ptr \[r8(?: \+ 8)?\]$", x.op_str) and x.mnemonic == "mov": mregs.add(x.op_str.split(",")[0])
        for r in mregs:
            m = re.search(r"\[%s \+ (0x[0-9a-f]+)\]" % r, x.op_str)
            if m and x.mnemonic in ("movzx", "mov", "test", "cmp"): mgr_reads.add((p, int(m.group(1), 16)))
def closure(a):
    seen = {a}; fr = [a]
    while fr:
        nx = []
        for f in fr:
            for x in body(f):
                if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
                    t = int(x.op_str, 16)
                    if t in SIZES and t not in seen and not f <= t < f + SIZES[f]: seen.add(t); nx.append(t)
        fr = nx
    return seen
cl = closure(0x358940) | closure(0x265380) | closure(0x3DBF60)
x100 = [(x.address) for f in cl for x in body(f) if re.search(r"\[r\w+ \+ 0x100\]", x.op_str) and "rsp" not in x.op_str]
check("R2 the four sync-verb escapes store {record, index}; their polls read only the manager byte +0x10, and the poll callees never touch +0x100",
      esc_ok and {o for _, o in mgr_reads} == {0x10} and x100 == [], "poll manager reads %s; closure %d functions, +0x100 accesses %d" % (sorted(mgr_reads), len(cl), len(x100)))

P = ROOT / "Database/FFXII TZA/_index/candidates/f1-weather-apply-thread/f1_thread_reach.py"
g = {"__file__": str(P)}; exec(compile(open(P, encoding="utf-8").read().split("APPLY = 0x26D910")[0], str(P), "exec"), g)
srcs = []
for c in sorted(g["callers"].get(0x2ED6F0, ())):
    ins = body(c)
    for k, x in enumerate(ins):
        if x.mnemonic in ("call", "jmp") and x.op_str == "0x2ed6f0":
            prev = [y for y in ins[max(0, k - 12):k] if y.op_str.split(",")[0].strip() in ("ecx", "rcx")]
            srcs.append((c, prev[-1].op_str if prev else "?"))
listy = [s for s in srcs if re.search(r"\*4 \+ [48]\]", s[1])]
t = dis(0x2EEEFE, 0x2EEF05)
fmt = [m.start() for m in re.finditer(rb"%c%0?\d?d", d)]
check("R3 no caller of the model-id decoder 002ED6F0 takes the id from a count-prefixed list; the letter table is static; no model-name format",
      len(srcs) >= 8 and listy == [] and t.get(0x2EEEFE) == "lea r12, [rip + 0xa2096b]" and 0x2EEF05 + 0xA2096B == 0xD0F870
      and len(fmt) == 1 and d[fmt[0]:fmt[0] + 8] == b"%c%d.efx",
      "%d call sites; list-shaped sources %d; format hits %d" % (len(srcs), len(listy), len(fmt)))
print("FAILS", fails)
sys.exit(1 if fails else 0)
