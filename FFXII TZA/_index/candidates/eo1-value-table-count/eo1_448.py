"""eo1_448.py - EO-1: when the settings object's +0x448 becomes 81 (FABLE, Claude Opus 5.5, 2026-09-26).

The config contract's section 4a (2026-09-10) and OPUS's CON-122 note (2026-09-20) already carry the answer; this
re-checks it on the bytes so the register row can say it.
  C1 the value 81 is written by exactly one instruction in the image: 001DF2A0 mov dword ptr [r8 + 0x448], 0x51, inside
     GameSettingConfig_InitializeValueTablesFromDefaults (001DF240).
  C2 001DF240 has one caller, 001DED50 at 001DEE3B, and that call is reached only through 001DED97 je 001DEE38, taken
     when the ini open returns a NULL handle, i.e. on a run that creates the settings file. The call is followed by
     the file write (001DEE43).
  C3 among the 64 functions that load the config global 01F82D20 (plus its constructor and loader), the only
     [reg+0x448] operands are that store and 001A24D4 lea rdi, [r15 + 0x448]. There r15 is 001A2130's own receiver,
     set once from rcx at 001A214A, so the lea is on another object.
So +0x448 is 81 only after a file-creating run's initialiser. Before that, and on every run that finds the file, it is
uninitialised malloc heap: the constructor's memset stops at +0x447 (contract section 4a).
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG
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
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
CFG = 0x01F82D20
writers81, callers, pop, acc = [], [], set(), []
for a, sz in F.items():
    o = off(a)
    if o is None or sz <= 0: continue
    L = list(cs.disasm(d[o:o + sz], a))
    uses = a in (0x1DE050, 0x1DED50, 0x1DF240)
    for x in L:
        ops = x.operands
        if x.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_MEM and ops[0].mem.disp == 0x448 \
                and ops[1].type == X86_OP_IMM and ops[1].imm == 0x51:
            writers81.append(x.address)
        if x.mnemonic in ("call", "jmp") and ops and ops[0].type == X86_OP_IMM and ops[0].imm == 0x1DF240:
            callers.append(x.address)
        if any(op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == "rip" and x.address + x.size + op.mem.disp == CFG for op in ops):
            uses = True
    if uses:
        pop.add(a)
        for x in L:
            for op in x.operands:
                if op.type == X86_OP_MEM and op.mem.disp == 0x448 and cs.reg_name(op.mem.base) not in ("rip", "rsp", "rbp"):
                    acc.append((x.address, "%s %s" % (x.mnemonic, x.op_str)))
check("C1 one instruction in the image writes 81 to +0x448: 001DF2A0", writers81 == [0x1DF2A0], str(["%08X" % a for a in writers81]))
S = {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x1DED50):off(0x1DED50) + F[0x1DED50]], 0x1DED50)}
check("C2 one caller, on the NULL-handle branch only, followed by the file write",
      callers == [0x1DEE3B] and S.get(0x1DED94) == "test rcx, rcx" and S.get(0x1DED97) == "je 0x1dee38"
      and S.get(0x1DEE3B) == "call 0x1df240" and S.get(0x1DEE43) == "call 0x1dfd40",
      "callers %s" % ["%08X" % a for a in callers])
S2 = {x.address: (x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x1A2130):off(0x1A2130) + F[0x1A2130]], 0x1A2130)}
r15w = [a for a, (m, o) in S2.items() if o.startswith("r15,") and m in ("mov", "lea", "pop", "xchg", "add", "sub")]
check("C3 the config users' only +0x448 operands are that store and a lea on 001A2130's own receiver",
      sorted(a for a, _ in acc) == [0x1A24D4, 0x1DF2A0] and r15w == [0x1A214A] and S2[0x1A214A] == ("mov", "r15, rcx"),
      "population %d; %s; r15 writes %s" % (len(pop), acc, ["%08X" % a for a in r15w]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
