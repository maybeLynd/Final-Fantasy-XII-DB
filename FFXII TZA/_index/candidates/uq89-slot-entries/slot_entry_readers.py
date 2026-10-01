"""slot_entry_readers.py - UQ-89: who touches the 40-byte entries of LegacyPs2GsTextureContext's table at +0x218
(FABLE, Claude Opus 5.5, 2026-09-26).

The context is one heap object cached at 0209A670 (types.tsv). Its table pointer lives at +0x218 and its count at +0x228.
  R1 every function that references 0209A670 (rip-relative), and every function that receives the loaded context as
     rcx in one of those bodies (one hop), is decoded; each access through [reg + 0x218] at any width is listed.
  R2 the only functions that touch +0x218 are the four in the context's own cluster: the initialiser 002F6AB0 (sets
     null), the rebuild 002F7380 (releases, allocates and writes 33 of each 40 bytes), the per-frame callback 002F4520
     (clears +0x00 and sets +0x20 = 0xFF), and the release callback 002F5450 (frees through 003EC8A0).
  R3 inside those four, the entry pointer is dereferenced only by stores: no instruction READS an entry field.
  R4 control: the census sees the rebuild's allocation store (002F75E1) and the per-frame loop's two loads of the table
     pointer (002F45F9 / 002F4604).
Blind spot, stated: code that reaches the context through a copy of the pointer held somewhere other than 0209A670,
or that indexes the entries from a pointer it received from none of these bodies, is not seen.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2])
    except (ValueError, IndexError): pass
def body(a): return list(cs.disasm(d[off(a):off(a) + F[a]], a)) if a in F and off(a) is not None else []
CTX = 0x209A670
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
# functions referencing the context global
refs = set()
for a in F:
    for x in body(a):
        for op in x.operands:
            if op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == "rip" and x.address + x.size + op.mem.disp == CTX:
                refs.add(a)
# one hop: callees handed the loaded context in rcx (mov reg,[CTX] ... mov rcx,reg ... call)
hop = set()
for a in refs:
    L = body(a); held = set()
    for x in L:
        ops = x.operands
        if x.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X86_OP_MEM and cs.reg_name(ops[1].mem.base) == "rip" \
                and x.address + x.size + ops[1].mem.disp == CTX:
            held.add(cs.reg_name(ops[0].reg))
        elif x.mnemonic == "mov" and len(ops) == 2 and ops[0].type == 1 and ops[1].type == 1 and cs.reg_name(ops[1].reg) in held:
            held.add(cs.reg_name(ops[0].reg))
        if x.mnemonic in ("call", "jmp") and ops and ops[0].type == X86_OP_IMM and "rcx" in held and ops[0].imm in F:
            hop.add(ops[0].imm)
CLUSTER = {0x2F6AB0, 0x2F7380, 0x2F4520, 0x2F5450}
scope = refs | hop | CLUSTER
touch = {}
for a in scope:
    for x in body(a):
        for k, op in enumerate(x.operands):
            if op.type == X86_OP_MEM and op.mem.disp == 0x218 and cs.reg_name(op.mem.base) not in ("rip", "rsp", "rbp"):
                touch.setdefault(a, []).append((x.address, "%s %s" % (x.mnemonic, x.op_str), k))
print("functions referencing 0209A670: %d; one-hop callees: %d" % (len(refs), len(hop - refs)))
for a in sorted(touch): print("  %08X: %s" % (a, ["%08X %s" % (s, t) for s, t, k in touch[a]]))
check("R2 only the context's own four functions touch +0x218", set(touch) <= CLUSTER and CLUSTER - {0x2F5450} <= set(touch) | {0x2F5450},
      str(sorted("%08X" % a for a in set(touch) - CLUSTER)))
# R3: inside the cluster, loads of the table pointer are followed only by stores through it
reads = []
for a in CLUSTER:
    L = body(a); tptr = set()
    VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
    for x in L:
        ops = x.operands
        if x.mnemonic == "mov" and len(ops) == 2 and ops[1].type == X86_OP_MEM and ops[1].mem.disp == 0x218:
            tptr.add(cs.reg_name(ops[0].reg)); continue
        for k, op in enumerate(ops):
            if op.type == X86_OP_MEM and cs.reg_name(op.mem.base) in tptr and k > 0 and x.mnemonic not in ("lea",):
                reads.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
        # a binding dies when its register is written, and volatile registers die across a call
        # (the FE-1 lesson: without both kills, a later unrelated [rax+k] reads as an entry access)
        try:
            _, wr = x.regs_access()
            for r in wr:
                nm = cs.reg_name(r)
                for full in list(tptr):
                    if nm == full or (full.startswith("r") and nm in (full.replace("r", "e", 1), full + "d")):
                        tptr.discard(full)
        except Exception:
            pass
        if x.mnemonic == "call":
            tptr -= VOL
check("R3 no instruction in the four reads an entry field through the table pointer", reads == [], str(reads[:4]))
S = {x.address: "%s %s" % (x.mnemonic, x.op_str) for a in CLUSTER for x in body(a)}
check("R4 control: the allocation store and the per-frame loads are seen",
      S.get(0x2F75E1) == "mov qword ptr [rdi + 0x218], rax" and S.get(0x2F45F9) == "mov rax, qword ptr [r14 + 0x218]"
      and S.get(0x2F4604) == "mov rax, qword ptr [r14 + 0x218]")
print("FAILS", fails)
sys.exit(1 if fails else 0)
