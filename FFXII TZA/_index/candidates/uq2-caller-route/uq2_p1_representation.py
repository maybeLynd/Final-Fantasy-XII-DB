"""UQ-2 residue: the REPRESENTATION of position 1 for the 321 rows that read rcx with no derived type (OPUS, 2026-09-27).

The class of a pointer is not derived here, and no meaning is claimed. What the callee's own body does with entry rcx is
enough to say what KIND of value position 1 is:
  POINTER  entry rcx (or a full 64-bit register copy of it) is the BASE of a memory operand
  INTn     no base use; the widest sub-register read of it (cl / cx / ecx) in an instruction other than a full copy -
           the callee consumes n bits, so position 1 is an n-bit integer
  WIDE64   only full 64-bit non-dereferencing uses (test rcx, rcx; a scale-1 index, where base and index are
           interchangeable) - pointer or 64-bit integer, not decided
  PASS     only handed on to a call or tail jump in an argument register - no local evidence
  NONE     no use found
Tracking is a MUST analysis over the CFG (intersection at joins); a call kills the volatile registers; any other write
kills.
  R  the classes over the 321: POINTER 151, INT32 78, INT16 36, INT8 19, WIDE64 16, PASS 19, NONE 2
  P  positive controls: 0031B770 is INT8 (`cmp cl, 0x27`, a BattleUnit getter's index); 0018D740 is POINTER (`mov dword
     ptr [rcx], edx`); 00197990 is INT32 (`mov ebx, ecx`)
  N  negative control: 00324020 uses entry rcx only as a scale-1 index (`[r8 + rbx + 0x194]`) and is NOT called a
     pointer (WIDE64)
With --write it writes uq2-p1-representation.tsv beside this file (addr, class, use counts).
Not claimed: the class a POINTER points at; signedness of the INTn; what any argument means.
"""
import collections, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
os.chdir(os.path.dirname(DB))
sys.path.insert(0, os.path.join(HERE, "..", "crr-flow-census"))
_a, sys.argv = sys.argv, sys.argv[:1]
import crr_flow_census as C
sys.argv = _a
from capstone import CS_OP_MEM, CS_OP_REG
ABI = os.path.join(DB, "00-Engine-Core-Runtime", "ABI-Recovery")
rows = [l.rstrip("\r\n").split("\t") for l in open(os.path.join(ABI, "derived-call-signatures.tsv"), encoding="utf-8")
        if l[:1].isalnum() and not l.startswith("addr")]
typed = set()
for fn in ("derived-signatures-this-types.tsv", "derived-signatures-ctor-types.tsv"):
    typed |= {l.split("\t")[0] for l in open(os.path.join(ABI, fn), encoding="utf-8") if l[:1].isalnum() and not l.startswith("addr")}
typed |= {"002FFEF0", "00306B10", "0030B8E0", "0030DA30"}     # uq2_caller_route.py C1
target = [r for r in rows if r[0] not in typed and r[1] != "0" and "rcx" in r[2].split(",")]
WIDTH = {}
for r64, subs in {"rax": ("eax", "ax", "al"), "rbx": ("ebx", "bx", "bl"), "rcx": ("ecx", "cx", "cl"), "rdx": ("edx", "dx", "dl"),
                  "rsi": ("esi", "si", "sil"), "rdi": ("edi", "di", "dil"), "rbp": ("ebp", "bp", "bpl")}.items():
    WIDTH[r64] = 8; WIDTH[subs[0]] = 4; WIDTH[subs[1]] = 2; WIDTH[subs[2]] = 1
for i in range(8, 16):
    WIDTH["r%d" % i] = 8; WIDTH["r%dd" % i] = 4; WIDTH["r%dw" % i] = 2; WIDTH["r%db" % i] = 1


def classify(f):
    xs = C.body(f)
    if not xs: return "NONE", {}
    bl, succ = C.blocks(xs)
    uses = collections.Counter()
    IN = {xs[0].address: frozenset(["rcx"])}; work = [xs[0].address]
    while work:
        a = work.pop(); st = set(IN[a])
        for x in bl[a]:
            ops = x.operands
            for op in ops:
                if op.type == CS_OP_MEM:
                    b = C.rn(op.mem.base) if op.mem.base else None
                    ix = C.rn(op.mem.index) if op.mem.index else None
                    if b in st: uses["POINTER"] += 1
                    elif ix in st: uses["INDEX"] += 1
            if x.mnemonic == "call":
                if st & {"rcx", "rdx", "r8", "r9"}: uses["PASS"] += 1
                for r in C.VOL: st.discard(r)
                continue
            if x.mnemonic == "jmp" and ops and ops[0].type != CS_OP_MEM and x.op_str.startswith("0x") and                     int(x.op_str, 16) in C.sizes and not (f <= int(x.op_str, 16) < f + C.sizes[f]):
                if st & {"rcx", "rdx", "r8", "r9"}: uses["PASS"] += 1     # a tail call hands the value on
                continue
            full_copy = (x.mnemonic == "mov" and len(ops) == 2 and ops[0].type == CS_OP_REG and ops[1].type == CS_OP_REG
                         and WIDTH.get(x.reg_name(ops[0].reg)) == 8 and WIDTH.get(x.reg_name(ops[1].reg)) == 8)
            if full_copy:
                s, d = C.rn(ops[1].reg), C.rn(ops[0].reg)
                if s in st: st.add(d)
                else: st.discard(d)
                continue
            try: rd, wr = x.regs_access()
            except Exception: rd, wr = [], []
            for r in rd:
                nm = x.reg_name(r)
                if C.rn(r) in st and nm in WIDTH:
                    if not any(op.type == CS_OP_MEM and (op.mem.base == r or op.mem.index == r) for op in ops):
                        uses["INT%d" % (8 * WIDTH[nm])] += 1
            for r in wr:
                k = C.rn(r)
                if k: st.discard(k)
        for s in succ[a]:
            n = frozenset(st)
            if s not in IN: IN[s] = n; work.append(s)
            else:
                m = IN[s] & n
                if m != IN[s]: IN[s] = m; work.append(s)
    if uses["POINTER"]: return "POINTER", dict(uses)
    ints = [k for k in uses if k.startswith("INT")] + (["INT64"] if uses["INDEX"] else [])
    if ints:
        v = max(ints, key=lambda k: int(k[3:]))
        return ("WIDE64" if v == "INT64" else v), dict(uses)
    return ("PASS" if uses["PASS"] else "NONE"), dict(uses)


out = [(r[0], *classify(int(r[0], 16))) for r in target]
cnt = collections.Counter(v for a, v, u in out)
by = {a: v for a, v, u in out}
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
check("R the classes over the 321", len(target) == 321 and cnt == {"POINTER": 151, "INT32": 78, "INT16": 36, "INT8": 19,
      "WIDE64": 16, "PASS": 19, "NONE": 2}, str(dict(cnt)))
check("P 0031B770 INT8, 0018D740 POINTER, 00197990 INT32",
      by.get("0031B770") == "INT8" and by.get("0018D740") == "POINTER" and by.get("00197990") == "INT32")
check("N 00324020 (entry rcx only a scale-1 index) is not called a pointer", by.get("00324020") == "WIDE64")
if "--write" in sys.argv:
    with open(os.path.join(HERE, "uq2-p1-representation.tsv"), "w", encoding="utf-8", newline="\n") as w:
        w.write("addr\tposition1\tuses\n")
        for a, v, u in sorted(out):
            w.write("%s\t%s\t%s\n" % (a, v, ",".join("%s:%d" % kv for kv in sorted(u.items()))))
    print("written uq2-p1-representation.tsv")
print("FAILS", fails)
sys.exit(1 if fails else 0)
