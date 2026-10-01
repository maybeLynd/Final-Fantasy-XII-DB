"""CharacterRenderRecord +0x10 is an 8-byte runtime pointer, and +0x14 / +0x16 are not fields of this record
(OPUS, 2026-09-27). Re-adjudicates OPUS-ADJUDICATE-THREE-WIDTH-DISAGREEMENTS-FOUND-BY-BLINDSPOT-12's third ruling
("a LONE OUTLIER ... the declared uint32 stands"), which weighed one qword READ against the dword reads and never looked
at the WRITER.

  W1 00420480's store to +0x10 is one QWORD (0042055B `mov qword ptr [rsi + 0x10], rbx`), rbx = r9 (004204A4, rbx not
     written between)
  W2 00420480's only caller, 004279B0, passes r9 = the return of 0020E600 (00427A56 -> 00427A5B `mov r9, rax` ->
     00427A71 call, r9 not written between)
  W3 0020E600 returns 64 bits: `mov eax, ecx; add rax, qword [01F83530]; ret` (ImageAddress_ResolveRuntimePointer)
  R1 0042DA5C reads the qword and dereferences it at once (0042DA60 `mov rcx, qword ptr [rcx + 0xd90]`)
  R2 every dword read of +0x10 in the flow receipt loads ecx and the next instruction that touches ecx / control flow is
     `call 0020E600` - the narrow readers re-resolve the low half; none uses the dword as a value
  P  in both flow receipts (flow-CharacterRenderRecord.tsv, crr-flow-accesses.tsv) nothing receiver-proven touches
     +0x14..+0x17 except the two qwords at +0x10
  X  the seven sites the 2026-09-22 pool-route census (db2e18c60) attributed to +0x14 / +0x16, all in 0053AB50, are on
     OTHER objects: reaching definitions (union at joins, copies followed through registers and rbp/rsp slots) give
     their base registers only the returns of 00521290 / 005212E0 (a 0x30-stride table), 0053B358 / 0053B3FE (a 32-bit
     computed base walked at 0xE0), 0053C627 (a 32-bit `add edi, r14d`), 0053C1F3 / 0053CE0A (a stack buffer)
  N  negative control: the same analysis gives 0053AC2E's `+0x284` read (a record access the flow census keeps) the
     pool formation 0053AC27 - the method can see the record in this function
  S  REGRESSION: the store declares +0x10 8 bytes and no row starts at +0x14 or +0x16 (FAILS before the correction)
Not claimed: what the pointer points at (0042DA5C reads its +0xD90), or whether the base 01F83530 can be >= 4 GiB (the
narrow readers would then lose the high half; CONTRACT-encoded-id-space-and-class-registry.md keeps that runtime).
"""
import csv, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
CAND = HERE.parent
DB = HERE.parents[2]
os.chdir(DB.parent)
sys.path.insert(0, str(CAND / "crr-flow-census"))
_argv, sys.argv = sys.argv, sys.argv[:1]
import crr_flow_census as C
sys.argv = _argv
from capstone import CS_OP_MEM, CS_OP_REG
args = sys.argv[1:]
FIELDS = Path(args[args.index("--fields") + 1]) if "--fields" in args else DB / "_types" / "fields.tsv"
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
def ins(f): return {x.address: x for x in C.body(f)}
def writes(x, reg):
    try: return any(C.rn(r) == reg for r in x.regs_access()[1])
    except Exception: return False
def between(f, a, b): return [x for x in C.body(f) if a < x.address < b]

# W1
b = C.body(0x420480); st10 = [x for x in b if any(o.type == CS_OP_MEM and o.access & 2 and o.mem.disp == 0x10 and C.rn(o.mem.base) == "rsi" for o in x.operands)]
I = ins(0x420480)
check("W1 00420480 stores +0x10 once, as a qword of rbx = r9", [x.address for x in st10] == [0x42055B] and st10[0].operands[0].size == 8
      and I[0x4204A4].mnemonic == "mov" and I[0x4204A4].op_str == "rbx, r9"
      and not any(writes(x, "rbx") for x in between(0x420480, 0x4204A4, 0x42055B)))
# W2
callers = [l.split("\t")[0] for l in open("Tools/work/graph/edges.tsv", encoding="utf-8") if l.split("\t")[1:2] == ["00420480"]]
J = ins(0x4279B0)
check("W2 the sole caller 004279B0 passes r9 = 0020E600's return", callers == ["004279B0"]
      and J[0x427A56].op_str == "0x20e600" and J[0x427A5B].op_str == "r9, rax" and J[0x427A71].op_str == "0x420480"
      and not any(writes(x, "r9") for x in between(0x4279B0, 0x427A5B, 0x427A71)), str(callers))
# W3
w3 = [(x.mnemonic, x.op_str) for x in C.body(0x20E600)]
check("W3 0020E600 = mov eax, ecx; add rax, qword [01F83530]; ret", len(w3) == 3 and w3[0] == ("mov", "eax, ecx") and w3[1][0] == "add"
      and w3[1][1].startswith("rax, qword ptr [rip") and 0x20E609 + int(w3[1][1].split("+ ")[1].rstrip("]"), 16) == 0x1F83530 and w3[2][0] == "ret")
# R1
K = ins(0x42DA30)
check("R1 0042DA5C reads the qword and dereferences it", K[0x42DA5C].op_str == "rcx, qword ptr [rcx + 0x10]" and K[0x42DA60].op_str == "rcx, qword ptr [rcx + 0xd90]")
# R2 / P
REC = [CAND / "type-flow-census" / "flow-CharacterRenderRecord.tsv", CAND / "crr-flow-census" / "crr-flow-accesses.tsv"]
rows = [a for a in csv.DictReader(open(REC[0], encoding="latin1"), delimiter="\t") if a["field"] == "0x10" and a["width"] == "4"]
bad = []
for a in rows:
    xs = C.body(int(a["function"], 16)); k = [i for i, x in enumerate(xs) if x.address == int(a["site"], 16)][0]
    res = None
    for y in xs[k + 1:k + 12]:
        if y.mnemonic == "call": res = y.op_str; break
        if y.mnemonic.startswith("j") or y.mnemonic == "ret" or writes(y, "rcx"): res = y.mnemonic + " " + y.op_str; break
    if not (xs[k].op_str.startswith("ecx, dword ptr") and res == "0x20e600"): bad.append(a["site"])
check("R2 every dword read of +0x10 feeds 0020E600 directly", rows and not bad, "(%d reads, %d not: %s)" % (len(rows), len(bad), bad[:5]))
cover = set()
for p in REC:
    for a in csv.DictReader(open(p, encoding="latin1"), delimiter="\t"):
        if a["field"].startswith("-"): continue
        o, w = int(a["field"], 16), int(a["width"])
        if o < 0x18 and o + w > 0x14: cover.add((a["site"], o, w))
check("P nothing receiver-proven touches +0x14..+0x17 but the two +0x10 qwords", cover == {("0042055B", 0x10, 8), ("0042DA5C", 0x10, 8)}, str(sorted(cover)))

# X / N: reaching definitions in 0053AB50
F = 0x53AB50; xs = C.body(F); bl, succ = C.blocks(xs); by = {x.address: x for x in xs}
def slot(op):
    bb = C.rn(op.mem.base) if op.mem.base else None
    return ("S", bb, op.mem.disp) if bb in ("rbp", "rsp") and not op.mem.index else None
def step(x, st):
    mn, ops = x.mnemonic, x.operands
    if mn == "call":
        for r in C.VOL: st[r] = frozenset([x.address])
        return st
    dst = C.rn(ops[0].reg) if ops and ops[0].type == CS_OP_REG else None
    full = dst is not None and C.cs.reg_name(ops[0].reg) == dst
    if mn == "mov" and len(ops) == 2 and ops[0].type == CS_OP_MEM and ops[1].type == CS_OP_REG and ops[0].size == 8 and slot(ops[0]):
        st[slot(ops[0])] = st.get(C.rn(ops[1].reg), frozenset(["in:" + C.rn(ops[1].reg)])); return st
    if mn == "mov" and full and ops[1].type == CS_OP_REG:
        st[dst] = st.get(C.rn(ops[1].reg), frozenset(["in:" + C.rn(ops[1].reg)])); return st
    if mn == "mov" and full and ops[1].type == CS_OP_MEM and slot(ops[1]):
        st[dst] = st.get(slot(ops[1]), frozenset(["slot:%X" % slot(ops[1])[2]])); return st
    try: w = x.regs_access()[1]
    except Exception: w = [ops[0].reg] if dst else []
    for r in w:
        k = C.rn(r)
        if k and k != "rsp": st[k] = frozenset([x.address])
    return st
IN = {xs[0].address: {}}; work = [xs[0].address]; at = {}
while work:
    a = work.pop(); st = dict(IN[a])
    for x in bl[a]: at[x.address] = dict(st); st = step(x, st)
    for s in succ[a]:
        if s not in IN: IN[s] = dict(st); work.append(s)
        else:
            m = dict(IN[s]); ch = False
            for k, v in st.items():
                u = m.get(k, frozenset()) | v
                if u != m.get(k): m[k] = u; ch = True
            if ch: IN[s] = m; work.append(s)
def producers(site):
    x = by[site]; op = [o for o in x.operands if o.type == CS_OP_MEM][0]
    return set(at[site].get(C.rn(op.mem.base), {"in"}))
SITES = {0x53B766: 0x14, 0x53B838: 0x14, 0x53BFE1: 0x14, 0x53C71E: 0x14, 0x53C18F: 0x16, 0x53C72D: 0x16, 0x53C85D: 0x16}
ALLOWED = {0x53B6CE, 0x53B6ED, 0x53B725, 0x53BF66, 0x53B358, 0x53B3FE, 0x53C627, 0x53C1F3, 0x53CE0A}
got = {s: producers(s) for s in SITES}
calls_ok = all(by[p].op_str in ("0x521290", "0x5212e0") for s in (0x53B766, 0x53B838, 0x53BFE1) for p in got[s])
check("X the seven +0x14 / +0x16 sites are on other objects (no pool formation, no record slot reaches them)",
      all(got[s] and got[s] <= ALLOWED and by[s].operands[[o.type for o in by[s].operands].index(CS_OP_MEM)].mem.disp == d
          for s, d in SITES.items()) and calls_ok,
      str({"%X" % s: sorted("%X" % p if isinstance(p, int) else p for p in v) for s, v in got.items()}))
check("N the same analysis ties 0053AC2E's +0x284 read to the pool formation 0053AC27", producers(0x53AC2E) == {0x53AC27})

# S
crr = {}
for l in FIELDS.read_bytes().decode("utf-8").splitlines():
    c = l.split("\t")
    if len(c) > 8 and c[0] == "CharacterRenderRecord": crr[int(c[1], 16)] = c
check("S the store declares +0x10 as 8 bytes and no row at +0x14 / +0x16",
      0x10 in crr and crr[0x10][2] == "8" and 0x14 not in crr and 0x16 not in crr,
      "(+0x10 %s; +0x14 %s; +0x16 %s)" % (crr.get(0x10, ["", "", "-"])[2], 0x14 in crr, 0x16 in crr))
print("FAILS", fails)
sys.exit(1 if fails else 0)
