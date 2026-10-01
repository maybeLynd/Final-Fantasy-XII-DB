"""SWE2-AUDIT-SEM own checks for FABLE's heading-delta alias note (9ca3df0ac).
H1 002E4380 from entry to its ret: where the input pointer is saved, where output bytes are cleared, where the input is
   read, and whether the decomposition path (from 002E4419) reads r9/r14.
H2 002E5030's call to 002E4380 (002E50CB): the output argument and the input argument.
H3 002E45E0 (963 B): every write to r14 / rbp / rbx / rsi / rdi, pushes/pops, and every direct callee.
H4 TRANSITIVE (beyond the record's direct-level limit): the call closure of 002E45E0 to depth 4 over direct calls and
   tail jumps (.pdata chain-root extents); in each body, a write to r14/r15/r12/r13/rbx/rbp/rsi/rdi that is not the
   restore of a save in the same body is reported (x64 non-volatile convention check). Indirect calls are counted.
   Positive control: 003DA6A0's rbp writes are seen and classified as saved."""
import struct, re, bisect
import img
PD = []
for n, rva, vsz, rp, rs in img.secs:
    if n == ".pdata":
        for k in range(0, vsz, 12):
            b, e, u = struct.unpack_from("<III", img.raw, rp + k)
            if b:
                PD.append((b + img.BASE, e + img.BASE, u + img.BASE))
PD.sort()
S = [p[0] for p in PD]
def root_of(b, u):
    uo = img.off(u)
    while uo is not None and (img.raw[uo] >> 3) & 4:
        cnt = img.raw[uo + 2]
        co = uo + 4 + ((cnt + 1) & ~1) * 2
        cb, ce, cu = struct.unpack_from("<III", img.raw, co)
        b = cb + img.BASE
        uo = img.off(cu + img.BASE)
    return b
ROOT = [root_of(b, u) for b, e, u in PD]
FR = {}
for k, (b, e, u) in enumerate(PD):
    FR.setdefault(ROOT[k], []).append((b, e))
def body(f):
    frs = FR.get(f)
    if not frs:
        xs = img.dis(f, 400)
        frs = [(f, xs[-1].address + xs[-1].size)]
    out = []
    for b, e in sorted(frs):
        out += list(img.md.disasm(img.rd(b, e - b), b))
    return out
def show(lo, hi):
    for x in img.md.disasm(img.rd(lo, hi - lo + 16), lo):
        if x.address > hi:
            break
        print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print("H1 002E4380 .. 002E4430"); show(0x002E4380, 0x002E4430)
print("H1b reads of r9/r14 at or after 002E4419 in 002E4380's body:",
      ["%08X %s %s" % (x.address, x.mnemonic, x.op_str) for x in body(0x002E4380) if x.address >= 0x002E4419 and re.search(r"\b(r9|r14)\w*\b", x.op_str)])
print("H2 002E5090 .. 002E50D0"); show(0x002E5090, 0x002E50D0)
NV = ("r14", "r15", "r12", "r13", "rbx", "rbp", "rsi", "rdi")
def norm(r):
    m = {"ebx": "rbx", "ebp": "rbp", "esi": "rsi", "edi": "rdi", "bx": "rbx", "bl": "rbx", "bp": "rbp", "bpl": "rbp",
         "si": "rsi", "sil": "rsi", "di": "rdi", "dil": "rdi"}
    if r in m:
        return m[r]
    mm = re.fullmatch(r"(r1[2-5])[dwb]?", r)
    return mm.group(1) if mm else r
def nonvol_report(f):
    xs = body(f)
    saved = set()
    for x in xs:
        o = [s.strip() for s in x.op_str.split(",")]
        if x.mnemonic == "push" and norm(o[0]) in NV:
            saved.add(norm(o[0]))
        m = re.match(r"qword ptr \[rsp \+ (0x[0-9a-f]+|\d+)\]$", o[0]) if o else None
        if x.mnemonic == "mov" and m and len(o) == 2 and norm(o[1]) in NV:
            saved.add(norm(o[1]))
        # frame-style save through r11 / rax = rsp
        if x.mnemonic == "mov" and len(o) == 2 and re.match(r"qword ptr \[r(11|ax) [+-] (0x[0-9a-f]+|\d+)\]$", o[0]) and norm(o[1]) in NV:
            saved.add(norm(o[1]))
    bad = []
    for x in xs:
        o = [s.strip() for s in x.op_str.split(",")]
        if not o or norm(o[0]) not in NV or x.mnemonic in ("push", "cmp", "test", "bt"):
            continue
        r = norm(o[0])
        if r not in saved:
            bad.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
    calls = set()
    ind = 0
    for x in xs:
        if x.mnemonic in ("call", "jmp"):
            if re.fullmatch(r"0x[0-9a-f]+", x.op_str):
                t = int(x.op_str, 16)
                if not (xs[0].address <= t <= xs[-1].address):
                    calls.add(t)
            elif x.mnemonic == "call":
                ind += 1
    return bad, calls, ind, len(xs)
print("H3 002E45E0 direct report")
bad, calls, ind, n = nonvol_report(0x002E45E0)
print("   instructions", n, "unsaved non-volatile writes:", bad, "direct targets:", len(calls), "indirect calls:", ind)
seen, frontier, depth_of = set(), [0x002E45E0], {0x002E45E0: 0}
viol, indirect = [], 0
while frontier:
    f = frontier.pop(0)
    if f in seen:
        continue
    seen.add(f)
    b, c, i, n = nonvol_report(f)
    indirect += i
    if b and f != 0x002E45E0:
        viol.append(("%08X" % f, depth_of[f], b[:4]))
    if depth_of[f] < 4:
        for t in c:
            if t not in depth_of:
                depth_of[t] = depth_of[f] + 1
                frontier.append(t)
print("H4 transitive closure to depth 4: %d functions, %d indirect calls inside them" % (len(seen), indirect))
print("H4 bodies with a non-volatile register written without a save in the same body: %d" % len(viol))
for v in viol:
    print("   ", v)
cb, cc, ci, cn = nonvol_report(0x003DA6A0)
print("CONTROL 003DA6A0 rbp writes classified saved:", not any("bp" in s for s in cb), [x for x in ["%08X %s %s" % (y.address, y.mnemonic, y.op_str) for y in body(0x003DA6A0)] if re.search(r"\b(rbp|ebp)\b", x.split(" ", 1)[1])][:6])
print("H5 002E5030 entry .. 002E5060 (where r14 comes from) and the call count in 002E45E0")
for x in img.md.disasm(img.rd(0x002E5030, 0x40), 0x002E5030):
    if x.address > 0x002E5060:
        break
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
xs = body(0x002E45E0)
print("H5 002E45E0 call instructions:", sum(1 for x in xs if x.mnemonic == "call"), " extent %08X-%08X" % (xs[0].address, xs[-1].address + xs[-1].size))
