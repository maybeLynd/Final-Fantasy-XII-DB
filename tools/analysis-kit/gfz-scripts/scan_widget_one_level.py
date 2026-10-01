"""Who writes Widget +0x38, +0x58, +0x60 and +0x80? The census proved nobody it could see does.

THE QUESTION THE CENSUS LEFT. widget-accesses.tsv records 13, 3, 21 and 3 LOADS at those four
offsets and NOT ONE STORE. The seed set includes the shared initialiser 002465F0, which clears
the object and writes none of them, so a writer exists outside the seed - the census said so
rather than pretending the fields are read-only.

THE BOUNDED WAY TO FIND IT. One level out, and admitted the same way the census admits its core
functions: for every seed function, find each `call` where a register PROVEN to hold the widget
is in RCX at the call, and look at the callee with RCX seeded as the widget. A callee reached
that way receives a widget in arg0 at least on that path.

WHY THAT IS NOT YET EVIDENCE, AND WHAT MAKES IT SO. A helper that takes a widget from one
handler also takes other types from elsewhere, so a store inside it is only a Widget store if
the widget is what reached it. This pass therefore reports, for every candidate writer, HOW MANY
DISTINCT SEED FUNCTIONS pass a widget into it in arg0. One caller is a coincidence waiting to be
read; a dozen handlers converging on the same helper is a shared setter. The number is printed
and nothing is declared from this script - it names the instructions a human then reads.

THE CONTROL. The same pass must rediscover writers at offsets the store already declares -
+0x40, +0x44, +0x48, +0xB4. Read it carefully: it finds writers at +0x40 (three, in two callees)
and +0x48 (one, in a callee 17 seed functions converge on) and NONE at +0x44 or +0xB4. That is
not a failure, and the distinction is the whole point of a control: the cited writers of +0x44
and +0xB4 are inside 002465F0, which is a SEED, so one level OUT is the wrong place to look for
them. The control shows the pass reaches writers that genuinely live one level out, and is
silent where the writer is already inside the seed.

THE NAME SAYS `scan_`, NOT `check_`, ON PURPOSE - run_gates.py collects `check_*` and this takes
minutes, and more importantly it is NOT A GATE: it produces leads a human then reads.

WHAT IT FOUND WHEN IT WAS WRITTEN, 2026-09-19, so the next reader starts from the answer and not
from the method:
  +0x58 and +0x60 were both answered by it. The acquire 002432B0 receives &widget+0x50 in RCX
    and writes the container's +0x00/+0x08/+0x10 - widget +0x50, +0x58, +0x60 - and the release
    002482E0 reads the same three back, frees the block at +0x60 through 003697F0 and nulls it.
    Both are now declared with both ends of the ownership named.
  +0x80 turned out to be a BITFIELD, not a plain dword: 002468A0 gates on bits 1..3, sets bit 0,
    and replaces bits 10..13 with a four-bit value.
  +0x38 WAS NOT ANSWERED. Thirteen handlers load it and three instruments have now failed to
    find a writer - the census, this pass, and the owner-side pass below. That is a bounded
    negative about three searches, not a claim that no writer exists.
  002468A0 also writes +0x84, +0x86, +0x8C, +0x8E, +0x90 and +0x94, none of them declared when
    this was written. Those are leads, not findings, until each is read.
"""
import collections
import io
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM, X86_OP_REG, X86_REG_RIP, X86_REG_R8
import reg_tracking as RT  # noqa: E402  (access direction: op_kind)

DB = "C:/Users/Kristian/source/repos/XIIOnline/Database"
EXE = DB + "/Tools/work/exe/FFXII_TZA.exe"
FUNCS = DB + "/Tools/work/graph/functions.tsv"
FIELDS = DB + "/FFXII TZA/_types/fields.tsv"
CTORS = (0x245000, 0x2465F0)
CORE = (0x2465F0, 0x245000, 0x245020, 0x273A20, 0x244F00, 0x2473B0, 0x247930, 0x248030, 0x244960)
WANT = (0x38, 0x58, 0x60, 0x80)
CONTROL = (0x40, 0x44, 0x48, 0xB4)
MAXD = 0xC0
CALLER_SAVED = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}

raw = open(EXE, "rb").read()
pe = struct.unpack_from("<I", raw, 0x3C)[0]
ns = struct.unpack_from("<H", raw, pe + 6)[0]
opt = struct.unpack_from("<H", raw, pe + 20)[0]
ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
off, secs = pe + 24 + opt, []
for _ in range(ns):
    nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
    vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((nm, ib + va, vs, rs, pr))
    off += 40


def fo(x):
    for nm, va, vs, rs, pr in secs:
        if va <= x < va + vs and (x - va) < rs:
            return pr + (x - va)
    return None


TLO = THI = 0
for nm, va, vs, rs, pr in secs:
    if nm == ".text":
        TLO, THI = va, va + vs

funcs = []
with io.open(FUNCS, encoding="utf-8") as fh:
    next(fh)
    for ln in fh:
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 3:
            try:
                funcs.append((int(c[0], 16), int(c[2])))
            except ValueError:
                pass
flen = dict(funcs)

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
cache = {}


def body(entry):
    if entry not in cache:
        n, f = flen.get(entry, 0), fo(entry)
        cache[entry] = [] if (f is None or n <= 0) else list(md.disasm(raw[f:f + n], entry))
    return cache[entry]


def norm(r):
    nm = md.reg_name(r)
    m = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi",
         "ebp": "rbp", "esp": "rsp", "ax": "rax", "bx": "rbx", "cx": "rcx", "dx": "rdx",
         "si": "rsi", "di": "rdi", "al": "rax", "bl": "rbx", "cl": "rcx", "dl": "rdx"}
    if nm in m:
        return m[nm]
    if nm and nm.startswith("r") and nm[-1] in "dwb" and nm[1:-1].isdigit():
        return "r" + nm[1:-1]
    return nm


self_ptr = set()
with io.open(FIELDS, encoding="utf-8") as fh:
    next(fh)
    for ln in fh:
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 5 and c[0] == "Widget" and c[4].strip() == "Widget*":
            self_ptr.add(int(c[1], 16))

handlers = set()
for entry, _ in funcs:
    r8 = None
    for i in body(entry):
        ops = i.operands
        if (i.mnemonic == "lea" and len(ops) == 2 and ops[0].type == X86_OP_REG
                and ops[0].reg == X86_REG_R8):
            t = None
            if ops[1].type == X86_OP_MEM and ops[1].mem.base == X86_REG_RIP:
                t = i.address + i.size + ops[1].mem.disp
            r8 = t if (t and TLO <= t < THI) else None
        elif (i.mnemonic in ("call", "jmp") and len(ops) == 1
                and ops[0].type == X86_OP_IMM and ops[0].imm in CTORS and r8):
            handlers.add(r8)


def walk(entry, report_calls, start=0, seed=("rcx",)):
    """MAY-taint entry with the widget in RCX. Returns (accesses, arg0_callees)."""
    ins = body(entry)
    if not ins:
        return [], []
    idx = {i.address: k for k, i in enumerate(ins)}
    succ = collections.defaultdict(set)
    for k, i in enumerate(ins):
        m = i.mnemonic
        tgt = i.operands[0].imm if (i.operands and i.operands[0].type == X86_OP_IMM) else None
        if m == "jmp":
            if tgt in idx:
                succ[k].add(idx[tgt])
        elif m.startswith("j"):
            if tgt in idx:
                succ[k].add(idx[tgt])
            if k + 1 < len(ins):
                succ[k].add(k + 1)
        elif m != "ret" and k + 1 < len(ins):
            succ[k].add(k + 1)
    state = [None] * len(ins)
    if start >= len(ins):
        return [], []
    state[start] = frozenset(seed)
    work, seen = [start], set()
    acc, calls = [], []
    while work:
        k = work.pop()
        cur = state[k]
        if cur is None:
            continue
        i = ins[k]
        if not i.mnemonic.startswith("nop"):
            for n_, op in enumerate(i.operands):
                if (op.type == X86_OP_MEM and op.mem.index == 0 and op.mem.base
                        and op.mem.base != X86_REG_RIP and norm(op.mem.base) in cur):
                    sig = (i.address, op.mem.disp, op.size)
                    if sig not in seen:
                        seen.add(sig)
                        kind = RT.op_kind(i, op, n_)
                        kind = "a" if kind == "addr" else kind
                        acc.append((i.address, op.mem.disp, op.size, kind,
                                    "%s %s" % (i.mnemonic, i.op_str)))
        if (report_calls and i.mnemonic == "call" and i.operands
                and i.operands[0].type == X86_OP_IMM and "rcx" in cur):
            calls.append((i.address, i.operands[0].imm))
        nxt = set(cur)
        m, ops = i.mnemonic, i.operands
        if m == "call":
            nxt -= CALLER_SAVED
        elif m == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG:
            d = norm(ops[0].reg)
            s = ops[1]
            if s.type == X86_OP_REG and norm(s.reg) in nxt:
                nxt.add(d)
            elif (s.type == X86_OP_MEM and s.size == 8 and s.mem.index == 0 and s.mem.base
                    and s.mem.base != X86_REG_RIP and norm(s.mem.base) in nxt
                    and s.mem.disp in self_ptr):
                nxt.add(d)
            else:
                nxt.discard(d)
        elif ops and ops[0].type == X86_OP_REG and m not in ("cmp", "test", "push"):
            nxt.discard(norm(ops[0].reg))
        nxt = frozenset(nxt)
        for s in succ[k]:
            if state[s] is None:
                state[s] = nxt
                work.append(s)
            elif not nxt <= state[s]:
                state[s] = state[s] | nxt
                work.append(s)
    return acc, calls


seeds = sorted(handlers | set(CORE))
callers = collections.defaultdict(set)
for s in seeds:
    _, calls = walk(s, True)
    for site, tgt in calls:
        if tgt in flen and tgt not in seeds:
            callers[tgt].add(s)

print("SEEDS %d.  CALLEES receiving a proven widget in RCX: %d" % (len(seeds), len(callers)))

writers = collections.defaultdict(list)
for cal in sorted(callers):
    acc, _ = walk(cal, False)
    for addr, disp, size, kind, txt in acc:
        if kind in ("w", "rw") and disp < MAXD:   # a read-modify-write is a writer too (priority 1, 2026-09-26)
            writers[disp].append((cal, len(callers[cal]), addr, txt))

print()
print("CONTROL  writers this pass finds at offsets the store already declares")
for d in CONTROL:
    ws = writers.get(d, [])
    print("  +0x%02X  %d writer instruction(s) in %d callee(s)"
          % (d, len(ws), len({w[0] for w in ws})))
    for cal, nc, addr, txt in ws[:4]:
        print("        %08X in %08X (reached from %d seed function(s))  %s" % (addr, cal, nc, txt))

print()
print("THE QUESTION  writers at the four read-only offsets")
for d in WANT:
    ws = writers.get(d, [])
    print("  +0x%02X  %d writer instruction(s) in %d callee(s)"
          % (d, len(ws), len({w[0] for w in ws})))
    for cal, nc, addr, txt in sorted(ws, key=lambda w: -w[1])[:8]:
        print("        %08X in %08X (reached from %d seed function(s))  %s" % (addr, cal, nc, txt))


# ---- the owner side: what the CONSTRUCTING function writes after the call -------------------
# 00245000 returns the object it constructed - `mov rbx, rcx` at 00245006 and `mov rax, rbx` at
# 00245016 - so RAX holds the widget at every return from it. Seeding the constructing function
# at the instruction after the call therefore starts from a proven widget, and picks up exactly
# the pattern the handlers already show: `call 00245000 ; mov rdi, rax ; ... mov [rdi+0x98], ax`.
owner = collections.defaultdict(list)
sites = 0
for entry, _ in funcs:
    ins = body(entry)
    for k, i in enumerate(ins):
        if (i.mnemonic == "call" and i.operands and i.operands[0].type == X86_OP_IMM
                and i.operands[0].imm == 0x245000):
            sites += 1
            acc, _ = walk(entry, False, k + 1, ("rax",))
            for addr, disp, size, kind, txt in acc:
                if kind in ("w", "rw") and disp < MAXD:   # a read-modify-write is a writer too (priority 1, 2026-09-26)
                    owner[disp].append((entry, addr, txt))

print()
print("THE OWNER SIDE  writes by the constructing function, seeded at RAX after %d `call 00245000`"
      % sites)
for d in sorted(owner):
    mark = "  <== one of the four" if d in WANT else ""
    print("  +0x%02X  %d write(s) in %d function(s)%s"
          % (d, len(owner[d]), len({w[0] for w in owner[d]}), mark))
for d in WANT + CONTROL:
    for entry, addr, txt in owner.get(d, [])[:6]:
        print("    +0x%02X  %08X in %08X  %s" % (d, addr, entry, txt))


# ---- the full one-level picture, by offset ------------------------------------------------
declared = set()
with io.open(FIELDS, encoding="utf-8") as fh:
    next(fh)
    for ln in fh:
        c = ln.rstrip("\n").split("\t")
        if len(c) >= 3 and c[0] == "Widget":
            o = int(c[1], 16)
            declared.update(range(o, o + int(c[2])))

allacc = collections.defaultdict(list)
for cal in sorted(callers):
    acc, _ = walk(cal, False)
    for addr, disp, size, kind, txt in acc:
        if disp < MAXD:
            allacc[disp].append((cal, len(callers[cal]), addr, size, kind, txt))

print()
print("ONE LEVEL OUT, EVERY OFFSET BELOW 0xC0, undeclared ones marked")
print("  %-7s %-4s %-6s %-5s %s" % ("disp", "n", "widths", "kinds", "callees (seed-callers)"))
for d in sorted(allacc):
    v = allacc[d]
    mark = "   <== UNDECLARED" if d not in declared else ""
    cs = sorted({(c, n) for c, n, _, _, _, _ in v}, key=lambda x: -x[1])
    print("  +0x%03X  %-4d %-6s %-5s %s%s"
          % (d, len(v), ",".join(str(s) for s in sorted({x[3] for x in v})),
             "".join(sorted({x[4] for x in v})),
             " ".join("%08X(%d)" % (c, n) for c, n in cs[:4]), mark))
