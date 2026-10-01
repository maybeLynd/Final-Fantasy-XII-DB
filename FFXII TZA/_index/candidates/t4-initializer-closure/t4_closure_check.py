"""T-4: does any C++ initializer rely on another translation unit's initializer having run first? (OPUS, 2026-09-27). Static.

FABLE's bound (2026-09-22) read each initializer's own body only. This follows every DIRECT call and tail jump to depth 4 from
each of the 1,172 __xc initializers (the set of shared globals is the same at depth 2 and 4) and classifies every global
written by one initializer and read, or address-formed, by a later one.

  C1 the table at 008C31D8 parses to 1,172 slots, all in the function list (FABLE's control)
  C2 the closure's shared writable globals (written by an initializer, used by a later one) number 72
  C3 every multi-writer global is one of: a CRT epoch (01F44850, _Init_thread_footer 0080929C); a function-local static
     built behind _Init_thread_header / _footer (01F2E330 / 01F2E340 / 01F2E358, guard 02CF94EC); or a read-modify-write
     accumulator whose one direct writer also reads it
  C4 14 of those accumulators are ONE compiland: one contiguous slot run and a .text run with no other function inside it
  C5 the two that cross compilands are order-independent in outcome:
       02CBF998, the named list of 005FDCB0 (first registrant of a name wins, a later one gets 0x12): all 116 init-time
       registrations (56 direct, 60 through 005DC6F0) have DISTINCT names, so the rejection path is never taken;
       02CF8260, the class-id counter (00632D80: +0xE8 = counter++): ids depend on order, and no instruction image-wide
       compares a dword at +0xE8 to a literal other than 0 / -1 except 0057F360, whose receiver is not a descriptor
       (its +0xC8 is a dword flag word; a descriptor's is a zeroed qword)
  C6 every use of a single-writer global by a later initializer is one of: the sixth argument of the descriptor
     constructor 00632D80 (stack +0x28), the root getter 006372A0 (lea rax, [02CF8270]; ret), or one of the intra-
     compiland pairs FABLE published (slots 356-365, 733 -> 735)
  R1 00632D80 stores its sixth argument at +0x78 (the parent pointer) and never dereferences it, so a later
     initializer holding an earlier one's descriptor address does not read what that initializer built. Together with
     C6 this REJECTS "some initializer reads another compiland's constructed object"
  P1 positive control: the published chain 00164180 (slot 356) -> 00163E30 (slot 358) through 02CF8270 is found
  L  residue, listed rather than claimed: indirect calls the closure does not follow. The allocator vtable 00902720
     (58 sites, via 001EDF00) is resolved - its allocate 001EDF80 builds its heap state 1F82E48 on first call, order-safe
     by construction - and the other 23 sites in 9 bodies (one, 0062CD40, a switch jump) are printed.
  L2 (second pass, 2026-09-27) the 23 sites RESOLVED, each by its own receiver:
     a  9 calls `[[X]+8]` on file-backed PUtility statics (0015BC40, 00792350) all sit behind `byte [01F2CDF0] == 0`; that
        byte is 1 in the file and its only references image-wide are 16 byte compares (no store, no lea), so they are
        skipped. Were one taken at slot 3 it would reach the file's vtable 00D26BC0 slot 1 = 005C5230 `xor eax, eax;
        ret`, because the derived vtables are installed only by slots 105-1171 (and exit handlers)
     b  0062CD40's `jmp rdx` is a 51-arm switch landing inside itself; the function reads no global
     c  0020D2F0 is the AMD ADL loader: its three indirect calls are GetProcAddress results from atiadlxx/atiadlxy, and the
        one in-image pointer it hands out, 0020D7B0, is `movsxd; jmp [malloc]`
     d  the allocator calls in 00199DB0 / 001E2250 / 001F57E0 go through words 001EDF00 installed (vtable 00902720,
        slots 2 / 3 = 001EDF80 / 001EDFE0)
     e  the element-destructor calls use the only vtables the reallocators install (009010B8 -> 009010D8 / 00903940),
        slot 0 of each
     f  006DA8A0 is dead at init: its only caller 00715360 (slot 656) calls it behind `[02EA0B58 + 8] != 0`, a .bss word
        no initializer before slot 656 writes or takes the address of
     g  re-run with those edges, the ONLY new shared global is the allocator heap state 01F82E48, built on first use by
        001EDF80 / 001EDFE0 (compare-to-zero, store on the zero path only) - order-safe - and the set is the same at depth
        6. That 01F82E48 appears at all is the positive control that the resolved edges were applied.
Not claimed: code outside the listed bodies; class ids that leave the process; and the one order-visible NUMBERING the
second pass found. 005FDCB0 inserts at the head of 02CBF998, so the list runs in reverse registration order, and 005FD560
numbers the nodes (+0x18 = 0, 1, 2, ...) by list position. The numbers therefore depend on cross-compiland init order.
The one consumer read here, 005F0720, uses a node's number only as a slot index into a per-object table sized by the
count (002CB635C), which is self-consistent. The other readers of node +0x18 are not enumerated.
"""
import struct, bisect, collections, json, sys, re
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import reg_tracking as RT
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64, CS_OP_MEM, CS_OP_IMM
from capstone.x86 import X86_REG_RIP, X86_REG_RCX, X86_REG_RDX

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) + (struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 36)[0],) for i in range(n)]
def off(v):
    for vs, va, rs, ro, ch in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
WR = [(BASE + va, BASE + va + max(vs, rs)) for vs, va, rs, ro, ch in SECS if ch & 0x80000000]
def writable(v): return any(a <= v < b for a, b in WR)
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except (ValueError, IndexError): pass
keys = sorted(sizes)
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
_b = {}
def body(f):
    if f not in _b:
        o = off(f); _b[f] = list(cs.disasm(d[o:o + sizes[f]], f)) if o is not None and sizes.get(f, 0) > 0 else []
    return _b[f]
INFO = {}
def info(f):
    if f not in INFO:
        r, w, a, calls = set(), set(), set(), set()
        for x in body(f):
            for oi, op in enumerate(x.operands):
                if op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP:
                    t = x.address + x.size + op.mem.disp
                    if not writable(t): continue
                    if x.mnemonic == "lea": a.add(t)
                    else:
                        k = RT.op_kind(x, op, oi)  # shared policy (OPUS 2026-09-28); 'addr' / '?' add to neither
                        if k in ("r", "rw"): r.add(t)
                        if k in ("w", "rw"): w.add(t)
            if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == CS_OP_IMM:
                t = x.operands[0].imm
                if t in sizes and not (f <= t < f + sizes[f]): calls.add(t)
        INFO[f] = (r, w, a, calls)
    return INFO[f]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok

TBL = 0x8C31D8
inits = [struct.unpack_from("<Q", d, off(TBL) + 8 * i)[0] for i in range(1172)]
check("C1 the table parses to 1,172 listed initializers", all(f in sizes for f in inits) and len(set(inits)) == 1172)

def closure(f, depth=4):
    seen = {f: 0}; q = [f]
    while q:
        g = q.pop(0)
        if seen[g] >= depth: continue
        for c in info(g)[3]:
            if c not in seen: seen[c] = seen[g] + 1; q.append(c)
    return seen
CL = [closure(f) for f in inits]
RW = []
for s, cl in enumerate(CL):
    R, W, A = set(), set(), set()
    for g in cl:
        r, w, a, _ = info(g); R |= r; W |= w; A |= a
    RW.append((R, W, A))
writers = collections.defaultdict(set)
for s, (R, W, A) in enumerate(RW):
    for g in W: writers[g].add(s)
shared = {g for s, (R, W, A) in enumerate(RW) for g in R | A if any(w < s for w in writers[g])}
d2 = set()
for s, f in enumerate(inits):
    R2, A2 = set(), set()
    for g in closure(f, 2):
        R2 |= info(g)[0]; A2 |= info(g)[2]
    d2 |= {g for g in R2 | A2 if any(w < s for w in writers[g])}
check("C2 72 shared globals, the same at depth 2 and 4", len(shared) == 72 and d2 == shared, "(%d, depth-2 %d)" % (len(shared), len(d2)))

allf = set().union(*[set(c) for c in CL])
multi = sorted(g for g in shared if len(writers[g]) > 1)
EPOCH, LOCALSTATIC = {0x1F44850}, {0x1F2E330, 0x1F2E340, 0x1F2E358}
acc, bad = [], []
for g in multi:
    dw = [f for f in allf if g in info(f)[1]]
    if g in EPOCH: ok = dw == [0x80929C]
    elif g in LOCALSTATIC:
        ok = all(any(x.mnemonic == "call" and x.op_str in ("0x8092fc", "0x80929c") for x in body(f)) for f in dw)
    else:
        ok = all(g in info(f)[0] for f in dw); acc.append(g)
    if not ok: bad.append("%08X" % g)
check("C3 every multi-writer global is the CRT epoch, a guarded local static or an RMW accumulator", not bad and len(acc) == 16,
      "(%d accumulators%s)" % (len(acc), "; bad " + " ".join(bad) if bad else ""))

def one_compiland(g):
    ws = sorted(writers[g]); fs = sorted(inits[s] for s in ws)
    return ws == list(range(ws[0], ws[-1] + 1)) and not [f for f in keys if fs[0] <= f <= fs[-1] and f not in set(fs)]
single = [g for g in acc if one_compiland(g)]; cross = sorted(set(acc) - set(single))
check("C4 14 accumulators are one compiland; 02CBF998 and 02CF8260 cross", len(single) == 14 and cross == [0x2CBF998, 0x2CF8260],
      "(cross: %s)" % " ".join("%08X" % g for g in cross))

# C5a names registered into 02CBF998 at init time
def cstr(v):
    o = off(v)
    if o is None: return None
    e = d.index(b"\0", o); return d[o:e].decode("latin1")
inits_set = set(inits); names = []
for f in allf:
    xs = body(f)
    for i, x in enumerate(xs):
        if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == CS_OP_IMM and x.operands[0].imm in (0x5FDCB0, 0x5DC6F0):
            for y in reversed(xs[max(0, i - 12):i]):
                if x.operands[0].imm == 0x5FDCB0 and y.mnemonic == "lea" and y.operands[0].reg == X86_REG_RCX and y.operands[1].mem.base == X86_REG_RIP:
                    node = y.address + y.size + y.operands[1].mem.disp; p = struct.unpack_from("<Q", d, off(node))[0]
                    names.append(cstr(p)); break
                if x.operands[0].imm == 0x5DC6F0 and y.mnemonic == "lea" and y.operands[0].reg == X86_REG_RDX and y.operands[1].mem.base == X86_REG_RIP:
                    names.append(cstr(y.address + y.size + y.operands[1].mem.disp)); break
names = [s for s in names if s]
# C5b literal compares on a dword at +0xE8
lit = []
for f in keys:
    if not (0x121000 <= f < 0x900000): continue
    xs = body(f)
    for i, x in enumerate(xs):
        o = x.operands
        if x.mnemonic == "cmp" and len(o) == 2 and o[0].type == CS_OP_MEM and o[0].mem.disp == 0xE8 and o[0].size == 4 and o[1].type == CS_OP_IMM and o[1].imm not in (0, -1, 0xFFFFFFFF):
            lit.append(f)
        if x.mnemonic == "mov" and len(o) == 2 and o[1].type == CS_OP_MEM and o[1].mem.disp == 0xE8 and o[1].size == 4 and o[0].type != CS_OP_MEM:
            r = x.reg_name(o[0].reg)
            if any(y.mnemonic == "cmp" and y.op_str.startswith(r + ",") and y.operands[1].type == CS_OP_IMM and y.operands[1].imm not in (0, -1, 0xFFFFFFFF) for y in xs[i + 1:i + 4]):
                lit.append(f)
flagword = any(x.mnemonic == "sub" and "[rdi + 0xd4]" in x.op_str for x in body(0x57F360)) and \
           any(x.mnemonic == "mov" and x.op_str == "dword ptr [rdi + 0xc8], ecx" for x in body(0x57F360))
check("C5 the cross-compiland accumulators are order-independent in outcome",
      len(names) == 116 and len(set(names)) == 116 and sorted(set(lit)) == [0x57F360] and flagword,
      "(%d names, %d distinct; literal +0xE8 compares in %s)" % (len(names), len(set(names)), " ".join("%08X" % f for f in sorted(set(lit)))))

# C6 / R1 uses of single-writer globals by later initializers
shapes = collections.Counter(); other = []
INTRA = {(356, 358), (356, 361), (356, 362), (356, 363), (356, 364), (356, 365), (358, 360), (733, 735)}
for g in sorted(shared):
    if len(writers[g]) != 1: continue
    w = min(writers[g])
    for s, (R, W, A) in enumerate(RW):
        if s <= w or not (g in R or g in A): continue
        for h in CL[s]:
            if g not in info(h)[2] and g not in info(h)[0]: continue
            xs = body(h)
            for i, x in enumerate(xs):
                if not any(op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP and x.address + x.size + op.mem.disp == g for op in x.operands): continue
                nx = xs[i + 1] if i + 1 < len(xs) else None
                call = next((y for y in xs[i + 1:i + 16] if y.mnemonic == "call"), None)
                if x.mnemonic == "lea" and nx is not None and nx.op_str.startswith("qword ptr [rsp + 0x28],") and call is not None and call.op_str == "0x632d80":
                    shapes["parent argument of 00632D80"] += 1
                elif h == 0x6372A0: shapes["root getter 006372A0"] += 1
                elif (w, s) in INTRA: shapes["published intra-compiland pair"] += 1
                else: other.append("%08X slot %d via %08X" % (g, s, h))
check("C6 every later use of a single-writer global is a parent argument, the root getter or a published intra pair",
      not other, "(%s%s)" % (dict(shapes), "; other " + "; ".join(other[:5]) if other else ""))
ctor = body(0x632D80)
arg6 = [i for i, x in enumerate(ctor) if x.op_str == "rax, qword ptr [rsp + 0x30]"]
deref = any(re.search(r"\[rax[ +\]]", x.op_str) and x.mnemonic != "lea" and "0x78" not in x.op_str for x in ctor[arg6[0] + 1:arg6[0] + 3]) if arg6 else True
check("R1 00632D80 stores its sixth argument at +0x78 and never dereferences it",
      len(arg6) == 1 and ctor[arg6[0] + 2].op_str == "qword ptr [rcx + 0x78], rax" and not deref
      and sum("rsp + 0x30" in x.op_str for x in ctor) == 1)
check("P1 the published chain 00164180 -> 00163E30 through 02CF8270 is found", 0x2CF8270 in shared
      and writers[0x2CF8270] == {356} and 0x2CF8270 in RW[358][2])

# L residue
vt = [struct.unpack_from("<Q", d, off(0x902720) + 8 * i)[0] for i in range(3)]
res = []
for f in sorted(allf):
    if 0x808000 <= f < 0x80A000: continue
    xs = body(f); uses_alloc = any(x.mnemonic == "call" and x.op_str == "0x1edf00" for x in xs)
    for x in xs:
        if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type != CS_OP_IMM and "rip" not in x.op_str and not uses_alloc:
            res.append("%08X %08X %s %s" % (f, x.address, x.mnemonic, x.op_str))
lazy = [x.op_str for x in body(0x1EDF80)]
check("L the allocator vtable resolves and its allocate is construct-on-first-use; the residue is listed",
      vt[2] == 0x1EDF80 and "qword ptr [rip + 0x1d94eba], 0" in lazy[2] and len(res) == 23 and len({r[:8] for r in res}) == 9,
      "(%d sites in %d bodies)" % (len(res), len({r[:8] for r in res})))
for r in res: print("      residue", r)

# L2 (OPUS, 2026-09-27, second pass): every residue site resolved, then the closure re-run with the resolved edges
q8 = lambda v: struct.unpack_from("<Q", d, off(v))[0]
def ripdst(x):
    for op in x.operands:
        if op.type == CS_OP_MEM and op.mem.base == X86_REG_RIP: return x.address + x.size + op.mem.disp
FILEB = [(BASE + va, BASE + va + rs) for vs, va, rs, ro, ch in SECS]
def filebacked(v): return any(a <= v < b for a, b in FILEB)
EXTRA = collections.defaultdict(set); why = {}
# (a) PUtility statics: `lea rcx, [X]; mov rax, [X]; call [rax + 8]`, X file-backed with vtable 00D26BC0, slot 1 = 005C5230
pu = {}
for f in (0x15BC40, 0x792350):
    xs = body(f)
    for i, x in enumerate(xs):
        if x.mnemonic == "call" and x.op_str == "qword ptr [rax + 8]":
            a, b = xs[i - 2], xs[i - 1]
            if a.mnemonic == "lea" and a.op_str.startswith("rcx,") and b.op_str.startswith("rax, qword ptr [rip") and ripdst(a) == ripdst(b):
                pu[x.address] = ripdst(a)
GUARD = 0x1F2CDF0
slot_of = {f: s for s, f in enumerate(inits)}
vt_writers = collections.defaultdict(set); guard_refs = []
for f in keys:
    if not (0x121000 <= f < 0x900000): continue
    for x in body(f):
        t = ripdst(x)
        if t is None: continue
        if GUARD - 7 <= t <= GUARD: guard_refs.append((x.mnemonic, x.op_str.split(",")[0]))
        for X in pu.values():
            if X <= t < X + 8 and not ((x.mnemonic == "lea" and x.op_str.startswith("rcx,")) or x.op_str.startswith("rax, qword ptr")):
                vt_writers[X].add(f)
guarded = all(any(y.mnemonic == "cmp" and ripdst(y) == GUARD for y in body(0x15BC40 if s < 0x200000 else 0x792350)
                  if s - 0x30 < y.address < s) for s in pu)
# every other reference to an object's vtable word is its dynamic initializer (a __xc slot after 3) or an exit-time
# handler outside the table (008A-008C); so at slot 3 the vtable word still holds the file's PUtility vtable
late = all(all((f in slot_of and slot_of[f] > 3) or (f not in slot_of and f >= 0x8A0000) for f in fs) for fs in vt_writers.values())
nop = [(x.mnemonic, x.op_str) for x in body(0x5C5230)]
check("L2a the 9 PUtility calls are skipped at init - guard byte 01F2CDF0 is 1 in the file and only ever compared (16 byte "
      "compares, no store, no lea); were they taken at slot 3 they would reach the file's vtable 00D26BC0 slot 1 = 005C5230 "
      "`xor eax, eax; ret`, the derived vtables being installed only by slots > 3",
      len(pu) == 9 and guarded and d[off(GUARD)] == 1 and len(guard_refs) == 16 and all(m == "cmp" and o == "byte ptr [rip" + o[13:] for m, o in guard_refs)
      and all(filebacked(X) and q8(X) == 0xD26BC0 for X in pu.values()) and q8(0xD26BC0 + 8) == 0x5C5230
      and nop == [("xor", "eax, eax"), ("ret", "")] and late,
      "(%d sites; vtable-word installers at slots %s)" % (len(pu), sorted(slot_of[f] for fs in vt_writers.values() for f in fs if f in slot_of)))
for s, X in pu.items(): EXTRA[0x15BC40 if s < 0x200000 else 0x792350].add(0x5C5230)
# (b) 0062CD40's `jmp rdx`: a 0x33-entry table of image-relative dwords at 0062CF0C, every target inside the function,
#     and the function has no other rip-relative operand
sw = body(0x62CD40); lo, hi = 0x62CD40, 0x62CD40 + sizes[0x62CD40]
tg = [BASE + struct.unpack_from("<I", d, off(0x62CF0C) + 4 * i)[0] for i in range(0x33)]
rips = [x for x in sw if ripdst(x) is not None]
check("L2b 0062CD40's switch lands inside itself on all 51 arms; it reads no global",
      any(x.op_str == "r8d, 0x32" for x in sw) and all(lo <= t < hi for t in tg) and len(rips) == 1 and ripdst(rips[0]) == BASE)
# (c) 0020D2F0 calls ADL exports: r9 = +0x30, +0x40, +0x48 are GetProcAddress results stored by this function from
#     atiadlxx.dll / atiadlxy.dll; the one in-image code pointer handed out, 0020D7B0, is `movsxd; jmp [IAT]`
import pefile
pef = pefile.PE(str(ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"), fast_load=True)
pef.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"]])
IAT = {i.address: (i.name or b"").decode() for e in pef.DIRECTORY_ENTRY_IMPORT for i in e.imports}
adl = body(0x20D2F0); st = {}
for i, x in enumerate(adl):
    m = re.match(r"qword ptr \[rdi \+ (0x[0-9a-f]+)\], rax", x.op_str)
    if x.mnemonic == "mov" and m and adl[i - 1].mnemonic == "call": st[int(m.group(1), 16)] = IAT.get(ripdst(adl[i - 1]), "?")
cb = [(x.mnemonic, x.op_str) for x in body(0x20D7B0)]
check("L2c 0020D2F0's three indirect calls are GetProcAddress results (+0x30/+0x40/+0x48); its callback 0020D7B0 jumps to an import",
      st.get(0x30) == st.get(0x40) == st.get(0x48) == "GetProcAddress" and st.get(0xB8) == "LoadLibraryW"
      and cb[0][0] == "movsxd" and cb[1][0] == "jmp" and IAT.get(0x20D7B3 + 7 + int(cb[1][1].split("+ ")[1].rstrip("]"), 16), "") != "",
      "(callback jumps to %s)" % IAT.get(0x20D7B3 + 7 + int(cb[1][1].split("+ ")[1].rstrip("]"), 16), "?"))
EXTRA[0x20D2F0].add(0x20D7B0)
# (d) allocator calls: 001EDF00 installs vtable 00902720 (slots 2 / 3 = 001EDF80 allocate / 001EDFE0 free) on the
#     allocator word the callers pass - vector +0x18 and map +0x30 of the objects 001E1520 / 001F4C50 construct
ctor = [x.op_str for x in body(0x1EDF00)]
wired = all(any(x.op_str == s for x in body(f)) for f, s in ((0x1E1520, "rcx, 0x18"), (0x1E1520, "rcx, [rbp + 0x30]"),
            (0x1F4C50, "rcx, [rbp + 0x30]"), (0x1E2250, "r9, qword ptr [rcx + 0x18]"), (0x1F57E0, "r9, qword ptr [rcx + 0x18]"),
            (0x199DB0, "rax, qword ptr [rcx + 0x30]")))
check("L2d the allocator calls resolve to 00902720 slots 2 / 3", ripdst(body(0x1EDF00)[0]) == 0x902720 and ctor[1] == "qword ptr [rcx], rax"
      and q8(0x902730) == 0x1EDF80 and q8(0x902738) == 0x1EDFE0 and wired)
for f in (0x199DB0, 0x1E2250, 0x1F57E0): EXTRA[f] |= {0x1EDF80, 0x1EDFE0}
# (e) element destructors: the only element vtables the reallocators install are 009010B8 then 009010D8 (001E2250) and
#     009010B8 then 00903940 (001F57E0); slot 0 of each
ev = {f: sorted({ripdst(x) for x in body(f) if x.mnemonic == "lea" and ripdst(x) and ripdst(x) >= 0x900000}) for f in (0x1E2250, 0x1F57E0)}
check("L2e the element vtables are 009010B8 / 009010D8 and 009010B8 / 00903940", ev == {0x1E2250: [0x9010B8, 0x9010D8], 0x1F57E0: [0x9010B8, 0x903940]}, str(ev))
dt = {v: q8(v) for v in (0x9010B8, 0x9010D8, 0x903940)}
EXTRA[0x1E2250] |= {dt[0x9010B8], dt[0x9010D8]}; EXTRA[0x1F57E0] |= {dt[0x9010B8], dt[0x903940]}
EXTRA[0x1E3D80] |= set(dt.values())
# (f) 006DA8A0 is reached only from 00715360 behind `test rdx, rdx; je` on [02EA0B58 + 8], a .bss word no earlier
#     initializer's closure writes or takes the address of
g = body(0x715360)
guard = [x.op_str for x in g[:8]]
dead_ok = "rdx, qword ptr [rcx + 8]" in guard and "rdx, rdx" in guard and not filebacked(0x2EA0B60)
_old_calls = {f: set(info(f)[3]) for f in list(INFO)}
for f, ts in EXTRA.items(): info(f)[3].update(t for t in ts if t in sizes)
CL2 = [closure(f) for f in inits]
early = set()
for s in range(656):
    for h in CL2[s]:
        r, w, a, _ = info(h); early |= (w | a) & {0x2EA0B58, 0x2EA0B60}
check("L2f 006DA8A0 is dead at init: its only caller's guard word 02EA0B60 is .bss and no initializer before slot 656 touches it",
      dead_ok and not early and ripdst(body(0x1689B0)[1]) == 0x2EA0B58)
RW2 = []
for s, cl in enumerate(CL2):
    R, W, A = set(), set(), set()
    for h in cl:
        r, w, a, _ = info(h); R |= r; W |= w; A |= a
    RW2.append((R, W, A))
writers2 = collections.defaultdict(set)
for s, (R, W, A) in enumerate(RW2):
    for h in W: writers2[h].add(s)
shared2 = {h for s, (R, W, A) in enumerate(RW2) for h in R | A if any(w < s for w in writers2[h])}
new = sorted(shared2 - shared)
print("      resolved edges:", {"%08X" % f: sorted("%08X" % t for t in ts) for f, ts in sorted(EXTRA.items())})
print("      new shared globals with the resolved edges:", ["%08X w%s" % (h, sorted(writers2[h])) for h in new])
HEAP = 0x1F82E48
allf2 = set().union(*[set(c) for c in CL2])
hw = sorted(f for f in allf2 if HEAP in info(f)[1])
def first_use(f):
    xs = body(f); c = [i for i, x in enumerate(xs) if ripdst(x) == HEAP]
    return (len(c) == 2 and xs[c[0]].op_str.startswith("qword ptr [rip") and xs[c[0]].mnemonic == "cmp" and xs[c[0]].op_str.endswith(", 0")
            and xs[c[0] + 2].mnemonic == "jne" and xs[c[1]].mnemonic == "mov" and xs[c[1]].address < xs[c[0] + 2].operands[0].imm)
CL6 = [closure(f, 6) for f in inits]
RW6 = [set().union(*[info(h)[0] | info(h)[2] for h in cl]) for cl in CL6]
W6 = collections.defaultdict(set)
for s, cl in enumerate(CL6):
    for h in cl:
        for gg in info(h)[1]: W6[gg].add(s)
shared6 = {h for s, R in enumerate(RW6) for h in R if any(w < s for w in W6[h])}
check("L2g with every residue edge resolved the only new shared global is the allocator heap state 01F82E48, built on first "
      "use by 001EDF80 / 001EDFE0 (compare-to-zero, store only on the zero path); the extended set is the same at depth 6",
      new == [HEAP] and hw == [0x1EDF80, 0x1EDFE0] and all(first_use(f) for f in hw) and shared6 == shared2,
      "(new %s; writers %s; depth-6 %d vs %d)" % (["%08X" % h for h in new], ["%08X" % f for f in hw], len(shared6), len(shared2)))
print("FAILS", fails)
raise SystemExit(1 if fails else 0)
