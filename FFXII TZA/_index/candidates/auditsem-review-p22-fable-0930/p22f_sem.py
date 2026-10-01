"""SWE2-AUDIT-SEM sample check of FABLE's pass-22 crossings (4407f8484): 19 UNACCOUNTED NEIGHBOUR pairs on 7 pages
(10 crossing sections, 9 registry rows).

Independent of the producer: its rebuild_edges.py / groups.py / apply.py / audit_crossrefs.py are NOT run. Bytes are
decoded here with capstone straight from the certified image (Tools/work/exe/FFXII_TZA.exe); edge existence is read
from Tools/work/graph/edges.tsv; verb names from the shipped verb table. Each check is one sentence of the package:
the far end named, the relationship it states, and the instruction sites it cites.

Run from the repo root:  python -B "Database/FFXII TZA/_index/candidates/auditsem-review-p22-fable-0930/p22f_sem.py"
"""
import csv
import os
import struct
import subprocess
import sys

import capstone
import pefile

ROOT = os.getcwd()
DBT = os.path.join(ROOT, "Database", "Tools")
EXE = os.path.join(DBT, "work", "exe", "FFXII_TZA.exe")
EDGES = os.path.join(DBT, "work", "graph", "edges.tsv")
VERBS = os.path.join(ROOT, "Database", "FFXII TZA", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")

pe = pefile.PE(EXE, fast_load=True)
data = pe.__data__
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
FAILS = []


def off(va):
    return pe.get_offset_from_rva(va - pe.OPTIONAL_HEADER.ImageBase)


def raw(va, n):
    o = off(va)
    return bytes(data[o:o + n])


def ins_at(va, n=1):
    return list(md.disasm(raw(va, 16 * n), va))[:n]


def body(va, stop_at_ret=True, limit=0x400):
    out = []
    for i in md.disasm(raw(va, limit), va):
        out.append(i)
        if stop_at_ret and i.mnemonic in ("ret", "jmp") and i == out[-1] and i.mnemonic == "ret":
            break
    return out


def run(va, end):
    """instructions from va up to (not past) end, linear."""
    return [i for i in md.disasm(raw(va, end - va + 16), va) if i.address <= end]


def rip(i):
    for op in i.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def target(i):
    if i.mnemonic in ("call", "jmp") and i.operands and i.operands[0].type == capstone.x86.X86_OP_IMM:
        return i.operands[0].imm
    return None


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""))
    if not ok:
        FAILS.append(name)


# edges.tsv (caller, callee)
E = set()
callers_of = {}
with open(EDGES, encoding="utf-8") as f:
    next(f)
    for ln in f:
        p = ln.rstrip("\r\n").split("\t")
        E.add((p[0], p[1]))
        callers_of.setdefault(p[1], set()).add(p[0])


def edge(a, b):
    return (a, b) in E


def calls_from(func, lo, hi, tgt):
    """does [lo, hi] inside func contain a call/jmp to tgt"""
    return any(target(i) == tgt for i in run(lo, hi))


# ---- R-a: the busy-bit pair (registry rows, how-a-script-changes-the-battle-party.md x3) --------------------------
b = run(0x003601B0, 0x003601BD)
check("Ra 003601B0 = mov eax,1; shl eax,cl; or [022CB720],eax; ret (14 B)",
      [i.mnemonic for i in b] == ["mov", "shl", "or", "ret"] and rip(b[2]) == 0x022CB720 and b[-1].address + 1 - 0x003601B0 == 14)
b = run(0x003601C0, 0x003601CF)
check("Ra 003601C0 = same with not/and (16 B)",
      [i.mnemonic for i in b] == ["mov", "shl", "not", "and", "ret"] and rip(b[3]) == 0x022CB720 and b[-1].address + 1 - 0x003601C0 == 16)
for c, t in (("002628B0", "003601B0"), ("003614E0", "003601B0"), ("00361460", "003601C0"), ("003145E0", "003601B0")):
    check(f"Ra edge {c} -> {t}", edge(c, t))

# ---- R-b: 00203170, the identity-matrix store (rig registry row; dispatch page) ------------------------------------
b = run(0x00203170, 0x0020319B)
srcs = [rip(i) for i in b if i.mnemonic == "movups" and rip(i)]
check("Rb 00203170 body is 44 B and copies four 16-byte rows to [rcx]",
      b[-1].mnemonic == "ret" and b[-1].address + 1 - 0x00203170 == 44 and len(srcs) == 4, "srcs=" + ",".join("%08X" % s for s in srcs))
rows = [struct.unpack("<4f", raw(s, 16)) for s in srcs]
check("Rb the four rows are the 4x4 identity", rows == [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)], str(rows))
check("Rb NOTE the sources are 008C5F80/90/B0/D0 (not a contiguous 64-byte run)", srcs == [0x008C5F80, 0x008C5F90, 0x008C5FB0, 0x008C5FD0])
ui = ["00247AE0", "002D2600", "002D28E0", "00368010", "003C5500", "003F26F0", "003F2A70"]
check("Rb the seven UI bodies call 00203170 (edges)", all(edge(u, "00203170") for u in ui), str([u for u in ui if not edge(u, "00203170")]))
check("Rb seteventlightdir 00356160 -> 00203170 (edge)", edge("00356160", "00203170"))

# ---- R-c: 001EDE70 the 60-fps gate --------------------------------------------------------------------------------
b = run(0x001EDE70, 0x001EDE76)
check("Rc 001EDE70 = mov eax,[01F82E38]; ret (7 B)", [i.mnemonic for i in b] == ["mov", "ret"] and rip(b[0]) == 0x01F82E38 and b[-1].address + 1 - 0x001EDE70 == 7)
check("Rc 00253C70 calls it at 00253D8F", target(ins_at(0x00253D8F)[0]) == 0x001EDE70)
check("Rc 22 direct callers (edges.tsv)", len(callers_of.get("001EDE70", ())) == 22, str(len(callers_of.get("001EDE70", ()))))

# ---- R-d: 001EDE80 step-count getter ------------------------------------------------------------------------------
b = run(0x001EDE80, 0x001EDEBC)
check("Rd 001EDE80 is 61 B: 1 when [01F82E38]==0 or [01DFE0C0]!=0, else 0022A080()+0022A030()",
      b[-1].address + 1 - 0x001EDE80 == 61 and rip(b[1]) == 0x01F82E38 and rip(b[3]) == 0x01DFE0C0
      and target(b[6]) == 0x0022A080 and target(b[8]) == 0x0022A030 and b[9].mnemonic == "add")
check("Rd 7 direct callers (edges.tsv)", len(callers_of.get("001EDE80", ())) == 7, str(len(callers_of.get("001EDE80", ()))))
seq = ins_at(0x0025DFA9, 4)
check("Rd 0025DF00 calls it at 0025DFA9 and branches to 0025E12B on 0",
      target(seq[0]) == 0x001EDE80 and any(i.mnemonic == "je" and i.operands[0].imm == 0x0025E12B for i in seq[1:]), " ; ".join(f"{i.mnemonic} {i.op_str}" for i in seq))
seq = ins_at(0x003FA7F8, 6)
check("Rd 003FA790 calls it at 003FA7F8 and a 0 skips 003FC170",
      target(seq[0]) == 0x001EDE80 and any(target(i) == 0x003FC170 for i in seq), " ; ".join(f"{i.mnemonic} {i.op_str}" for i in seq))

# ---- R-e: 001A1470 x3 from the render pass list ---------------------------------------------------------------------
for s in (0x00187AB5, 0x00187AFE, 0x00187B4F):
    pre = run(s - 0x18, s)
    i = [x for x in pre if x.address == s]
    heap = any(rip(x) == 0x01F7F4C0 for x in pre)
    sz = any(x.mnemonic == "mov" and x.op_str.startswith("edx") and x.op_str.endswith("0x10") for x in pre)
    check(f"Re 00187950 calls 001A1470 at {s:08X} with [01F7F4C0] and size 0x10",
          bool(i) and target(i[0]) == 0x001A1470 and heap and sz, " ; ".join(f"{x.mnemonic} {x.op_str}" for x in pre[-4:]))
check("Re 001A1470 has 35 direct callers (edges.tsv)", len(callers_of.get("001A1470", ())) == 35, str(len(callers_of.get("001A1470", ()))))

# ---- R-f: 005FD050 from four D3D11 backend bodies -------------------------------------------------------------------
for c in ("0061F200", "0061F710", "006209C0", "006239C0"):
    check(f"Rf edge {c} -> 005FD050", edge(c, "005FD050"))
check("Rf 005FD050 has 55 direct callers (edges.tsv)", len(callers_of.get("005FD050", ())) == 55, str(len(callers_of.get("005FD050", ()))))

# ---- S1: 00236760 / 00236780 flag-bit getters and the save layer (field map) ---------------------------------------
for a, n in ((0x00236760, 12), (0x00236780, 14)):
    b = run(a, a + 0x10)
    check(f"S1 {a:08X} = mov rax,[02EBF190]; mov eax,[rax+4]; shr eax,{n}; and eax,1; ret",
          rip(b[0]) == 0x02EBF190 and b[1].op_str == "eax, dword ptr [rax + 4]" and b[2].op_str == f"eax, {hex(n)}" and b[3].op_str == "eax, 1" and b[4].mnemonic == "ret")
for s, t in ((0x001C1758, None), (0x002EF696, None)):
    i = ins_at(s)[0]
    check(f"S1 call site {s:08X} calls 00236760 or 00236780", target(i) in (0x00236760, 0x00236780), f"{i.mnemonic} {i.op_str}")
blk = run(0x00583F5A, 0x00583F70)
txt = " ; ".join(f"{i.mnemonic} {i.op_str}" for i in blk)
check("S1 00583D60 ORs header +0x57 with 1 and 4 (00583F5A-00583F70)",
      any(target(i) in (0x00236760, 0x00236780) for i in blk) and "0x57" in txt and (", 1" in txt) and (", 4" in txt), txt)

# ---- S2: 00290180 and is_ntsc (gamepad page) -------------------------------------------------------------------------
b = run(0x00290180, 0x00290185)
check("S2 00290180 = mov eax,2; ret (6 B)", [i.op_str for i in b] == ["eax, 2", ""] and b[-1].address + 1 - 0x00290180 == 6)
verbs = {r["verb"]: r for r in csv.DictReader(open(VERBS, encoding="utf-8"), delimiter="\t")}
v = verbs.get("is_ntsc", {})
check("S2 is_ntsc is verb 0x4EB with handler 003423E0 (verb table)",
      int(v.get("call_id", "0"), 16) == 0x4EB and "003423E0" in (v.get("begin", ""), v.get("arg_handler", "")), str({k: v.get(k) for k in ("call_id", "begin", "arg_handler")}))
blk = run(0x003423E9, 0x003423F6)
check("S2 003423E9-003423F6: calls 00290180 and compares with 2",
      any(target(i) == 0x00290180 for i in blk) and any(i.mnemonic == "cmp" and i.op_str.endswith(", 2") for i in blk),
      " ; ".join(f"{i.mnemonic} {i.op_str}" for i in blk))

# ---- S3: 00264670 (effect frame page, dispatch page) -----------------------------------------------------------------
b = run(0x00264670, 0x00264692)
check("S3 00264670 is 35 B: class 3 ([+3]&0xE0==0x60) -> float [[+0xB8]+0xD4], else 0.0",
      b[-1].address + 1 - 0x00264670 == 35 and any(i.op_str.endswith("0x60") for i in b) and any("0xb8" in i.op_str for i in b)
      and any("0xd4" in i.op_str for i in b) and any(i.mnemonic == "xorps" for i in b))
check("S3 floor probe 002F3750 -> 00264670 (edge)", edge("002F3750", "00264670"))
check("S3 getgroundy handler 00343520 -> 00264670 (edge + verb table)",
      edge("00343520", "00264670") and "00343520" in (verbs.get("getgroundy", {}).get("begin", ""), verbs.get("getgroundy", {}).get("arg_handler", "")))

# ---- S4: 00265090 and the loot test (reach page) ---------------------------------------------------------------------
b = run(0x00265090, 0x002650AA)
check("S4 00265090: class 3 -> tail-jump with rcx=[+0xB8]+0x50 (00265090-002650A5)",
      any("0xb8" in i.op_str for i in b) and any(i.mnemonic == "add" and i.op_str == "rcx, 0x50" for i in b) and target(b[-2]) is not None and b[-2].mnemonic == "jmp")
check("S4 002FB150 calls 00265090 at 002FB1C1", target(ins_at(0x002FB1C1)[0]) == 0x00265090)

# ---- S5: 003E7650's only caller (rig page) ---------------------------------------------------------------------------
check("S5 003E7650 has exactly one caller, 00314020 (edges.tsv)", callers_of.get("003E7650") == {"00314020"}, str(callers_of.get("003E7650")))
check("S5 the site is 00314341", target(ins_at(0x00314341)[0]) == 0x003E7650)

# ---- S6: 00182E80 display-height getter (post-effect page) -----------------------------------------------------------
b = run(0x00182E80, 0x00182EA8)
check("S6 00182E80 is 41 B; null -> 0x438", b[-1].address + 1 - 0x00182E80 == 41 and any(i.op_str == "eax, 0x438" for i in b))
g = run(0x001DDAB0, 0x001DDAB0 + 8)
check("S6 001DDAB0 returns [01F82D18]", rip(g[0]) == 0x01F82D18 and g[1].mnemonic == "ret", f"{g[0].mnemonic} {g[0].op_str}")
h = run(0x002256A0, 0x002256A0 + 8)
check("S6 002256A0 returns dword [rcx+0x14]", h[0].op_str == "eax, dword ptr [rcx + 0x14]" and h[1].mnemonic == "ret", f"{h[0].mnemonic} {h[0].op_str}")
check("S6 00187950 calls 00182E80 at 00187993", target(ins_at(0x00187993)[0]) == 0x00182E80)

# ---- S7: dispatch page accessors ---------------------------------------------------------------------------------------
check("S7 0053DD10 = mov eax,1; ret", [i.op_str for i in run(0x0053DD10, 0x0053DD15)] == ["eax, 1", ""])
check("S7 003590D0 = mov eax,[022C7FE0]; ret (7 B)", rip(run(0x003590D0, 0x003590D6)[0]) == 0x022C7FE0)
# the pair is (page, Script_VM_Native_Bridge): count callers whose ledger owner is that layer (functions.tsv)
FUNCS = os.path.join(DBT, "work", "graph", "functions.tsv")
owner = {r["entry"]: r["owner"] for r in csv.DictReader(open(FUNCS, encoding="utf-8"), delimiter="\t")}
tot, uniq = 0, set()
for acc, n in (("00265020", 23), ("0053DD10", 17), ("003590D0", 14), ("00203170", 1), ("00264670", 1), ("0036A100", 1)):
    k = sorted(c for c in callers_of.get(acc, ()) if owner.get(c) == "Script_VM_Native_Bridge")
    tot += len(k)
    uniq |= set(k)
    check(f"S7 {acc}: Script_VM_Native_Bridge-owned callers in edges.tsv = {n}", len(k) == n, f"found {len(k)}")
check("S7 57 edges from 54 distinct handlers", tot == 57 and len(uniq) == 54, f"edges={tot} handlers={len(uniq)}")
# a verb-table control: the 17 0053DD10 callers are all verb handlers (begin/poll/slot2/arg_handler)
hv = set()
for r in verbs.values():
    for k_ in ("begin", "poll", "slot2", "arg_handler"):
        if r.get(k_):
            hv.add(r[k_])
k = [c for c in callers_of.get("0053DD10", ()) if owner.get(c) == "Script_VM_Native_Bridge"]
check("S7 control: every script-layer caller of 0053DD10 is a verb-table handler", all(c in hv for c in k))
i = ins_at(0x00341876)[0]
check("S7 modelreadsync's test at 00341876 is on 0053DD10's answer", i.mnemonic in ("test", "cmp") and target(ins_at(0x00341876 - 5)[0]) == 0x0053DD10,
      f"{i.mnemonic} {i.op_str}")
check("S7 modelreadsync 00341840 -> 0053DD10 (edge)", edge("00341840", "0053DD10"))
check("S7 debug_tkmalloc_4 0050D8F0 -> 0036A100 (edge)", edge("0050D8F0", "0036A100"))

# ---- S8: field-map CombatFormula / Items (sites) -----------------------------------------------------------------------
blk = run(0x0031B87D, 0x0031B8A4)
check("S8 0031B860 compares [unit+0x698] in 0031B87D-0031B8A4", any("0x698" in i.op_str for i in blk), " ; ".join(f"{i.mnemonic} {i.op_str}" for i in blk[:8]))
i = ins_at(0x003244E1)[0]
check("S8 00324470 sets unit flag bit 6 at 003244E1 (or dword [rbx], 0x40)", i.mnemonic == "or" and i.op_str == "dword ptr [rbx], 0x40", f"{i.mnemonic} {i.op_str}")
blk = run(0x00324398, 0x003243CC)
check("S8 00324380 rebuilds 022C257C from [+0x698]+4 (00324398-003243CC)",
      any(rip(x) == 0x022C257C for x in run(0x00324380, 0x003243CC)) and any("0x698" in x.op_str for x in blk), " ; ".join(f"{x.mnemonic} {x.op_str}" for x in blk[:10]))
blk = run(0x003906BD, 0x003906CE)
check("S8 00390680 reads [unit+0xE60] (003906BD-003906CE)", any("0xe60" in x.op_str for x in blk))
blk = run(0x00300BDD, 0x00300BF0)
check("S8 F3: 00300BC0 finds the unit (0031B860) then calls 0030B770 (00300BDD-00300BF0)",
      any(target(x) == 0x0031B860 for x in run(0x00300BC0, 0x00300BF0)) and any(target(x) == 0x0030B770 for x in blk),
      " ; ".join(f"{x.mnemonic} {x.op_str}" for x in blk))
blk = run(0x00386C2E, 0x00386C3F)
check("S8 F5: 00386C10 caches the unit at 02EBF188 and reads +0xEA9 (00386C2E-00386C3F)",
      any(rip(x) == 0x02EBF188 for x in blk) and any("0xea9" in x.op_str for x in blk), " ; ".join(f"{x.mnemonic} {x.op_str}" for x in blk))
for s in (0x00320A4B, 0x00320AC7):
    i = ins_at(s)[0]
    check(f"S8 F2: imul 0x1C8 at {s:08X}", i.mnemonic == "imul" and i.op_str.endswith("0x1c8"), f"{i.mnemonic} {i.op_str}")

# ---- S9: RNG section -----------------------------------------------------------------------------------------------------
for s in (0x002356A3, 0x003081FF, 0x00239547):
    i = ins_at(s)[0]
    check(f"S9 {s:08X} calls 00328370", target(i) == 0x00328370, f"{i.mnemonic} {i.op_str}")
for c in ("00386C70", "00388660"):
    check(f"S9 {c} -> 00379CD0 (edge)", edge(c, "00379CD0"))
check("S9 00308EC0 -> 00328370 (edge)", edge("00308EC0", "00328370"))

# ---- H: the two consumers the package routed to "FABLE-P22-FOLLOWUP" (no board task) - state at HEAD -----------------
DBP = os.path.join(ROOT, "Database", "FFXII TZA")


def head(path):
    return subprocess.run(["git", "show", "HEAD:Database/FFXII TZA/" + path], capture_output=True, check=True).stdout.decode("utf-8")


sl = head("17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md")
check("H1 finding: staged-look page still calls 00203170 'the per-slot visitor' (unstruck at HEAD)",
      "`00203170`, the per-slot visitor this page's `003E3C30` section names" in sl)
blk = run(0x003E3C30, 0x003E3C9C)
check("H1 counter-evidence: 003E3C30 is the visitor - it loops and calls 00203170 per slot at 003E3C7A",
      target(ins_at(0x003E3C7A)[0]) == 0x00203170 and any(x.mnemonic in ("jl", "jb", "jne", "jae", "jge") and x.operands[0].imm < 0x003E3C7A for x in blk if x.operands and x.operands[0].type == capstone.x86.X86_OP_IMM))
fm = head("04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md")
check("H2 finding: field map section 11 still says '`00236780` is the shared RNG/roll helper' unstruck at HEAD",
      "`00236780` is the shared RNG/roll helper" in fm and "~~`00236780` is the shared RNG/roll helper" not in fm)

print("FAILS", len(FAILS))
sys.exit(1 if FAILS else 0)
