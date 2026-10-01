"""falsify_encoded_id.py - falsification pass 1 on CONTRACT-encoded-id-space-and-class-registry.md (OPUS, 2026-09-30).

Each check turns one of the contract's static clauses into a test at its instructions or data in the shipping image
(sha 73461d08...). A check prints SURVIVES or BROKEN with what it measured. Reads only.

E1  §2 00309440: low 16 bits, nibble 0..E into 01EEBCC0 + n*0x58 + 0x38, nibble F returns -1
E2  §3 the registry table: +0x38 = nibble + 5; +0x3C counts sum 6892; pointer lanes and prefixes zero on disk; offset
    high halves zero; handlers: classes 14/15/18/19 mutate-only (002FD530/002FD640/002FD780/002FD880), 10/12/16 none
E3  §6 the validator: a 32-entry image-relative table at 00323054, every target inside the validator; the shared tail
    at 0032302E / 00323036 / 00323039 / 00323041
E4  I2 class 19 admits E000..EFFE inclusive
E5  §2 the filler 0031C5D0: a 32-entry table at 0031E598; class 12's arm returns -2 without reading either input lane
E6  §2 the wrappers 0035D330 / 0035D380: their records 022CA520 (+0 tag, +4 dword) and 022CA480 (+0 tag, +6 word); a
    negative fill calls 0016D6A0 and clears 0x98 bytes; both return the record address
E7  I4 the rebase 0030B6A0 clears state+57C8 for 0x200 bytes and ANDs 128 bytes from state+59C8 with F8
E8  §6 0020E600 returns the zero-extended dword plus the full qword at 01F83530
E9  I1 the input lane each class's query arm reads first: WORD+6 for 1,5..11,13..18,30,31; DWORD+4 for 2..4,19..29,32
E10 §14 "The only functions that address the table are the rebase 0030B6A0 and 0030B270"
"""
import collections, io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402  (image access and decoder)
from capstone import x86 as X  # noqa: E402

at, md, ext, BASE = R.at, R.md, R.ext, R.b.BASE
REG = 0x01EEBCC0
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def body(f, n=None):
    return list(md.disasm(at(f, n or ext[f]), f))


def rip_target(i, k):
    op = i.operands[k]
    return i.address + i.size + op.mem.disp if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP else None


def u32(a):
    return struct.unpack("<I", at(a, 4))[0]


def u64(a):
    return struct.unpack("<Q", at(a, 8))[0]


# E1
b = body(0x00309440)
txt = " | ".join("%s %s" % (i.mnemonic, i.op_str) for i in b)
refs = set(rip_target(i, k) for i in b for k in range(len(i.operands)) if rip_target(i, k))
has_shift = any(i.mnemonic in ("shr", "sar") and i.op_str.endswith("0xc") for i in b)
has_minus1 = any(("0xffffffff" in i.op_str or i.op_str.endswith(", -1")) for i in b)
has_stride = "0x58" in txt
check("E1", has_shift and has_minus1 and has_stride and any(r in (REG, REG + 0x38) for r in refs),
      "00309440 (%d instrs): shift by 12 %s, -1 path %s, stride 0x58 %s, table ref %s" % (
          len(b), has_shift, has_minus1, has_stride, " ".join("%08X" % r for r in sorted(refs))))

# E2
rows = [REG + n * 0x58 for n in range(15)]
cls = [u32(r + 0x38) for r in rows]
cnt = [u32(r + 0x3C) for r in rows]
lanes_zero = all(u64(r + o) == 0 for r in rows for o in (0x08, 0x20, 0x30)) and all(u32(r + 0x40) == 0 for r in rows)
hi_zero = all(u32(r + o + 4) == 0 for r in rows for o in (0x00, 0x18, 0x28))
h = {n + 5: (u64(r + 0x48), u64(r + 0x50)) for n, r in enumerate(rows)}
mut_only = {c for c, (m, q) in h.items() if m and not q}
none_ = {c for c, (m, q) in h.items() if not m and not q}
mut_ptrs = [h[c][0] for c in (14, 15, 18, 19)]
check("E2", cls == [n + 5 for n in range(15)] and sum(cnt) == 6892 and lanes_zero and hi_zero
      and mut_only == {14, 15, 18, 19} and none_ == {10, 12, 16}
      and mut_ptrs == [0x002FD530, 0x002FD640, 0x002FD780, 0x002FD880],
      "classes %s; counts sum %d; pointer lanes/prefixes zero %s; offset high halves zero %s; mutate-only %s %s; none %s" % (
          cls, sum(cnt), lanes_zero, hi_zero, sorted(mut_only), " ".join("%08X" % p for p in mut_ptrs), sorted(none_)))

# E3
V = 0x00322C50
vend = V + ext[V]
vt = [BASE + u32(0x00323054 + 4 * k) for k in range(32)]
in_v = all(V <= t < vend for t in vt)
tail = {a: R.dec(a) for a in (0x0032302E, 0x00323036, 0x00323039, 0x00323041)}
tail_ok = (tail[0x0032302E].mnemonic == "cmp" and tail[0x0032302E].op_str == "ebx, edx"
           and tail[0x00323036].mnemonic == "lea" and tail[0x00323036].op_str == "eax, [rcx - 1]"
           and tail[0x00323039].mnemonic == "cmp" and tail[0x00323039].op_str == "ebx, eax"
           and tail[0x00323041].mnemonic == "mov" and tail[0x00323041].op_str == "eax, 1")
check("E3", in_v and tail_ok, "validator table: 32 targets all inside 00322C50 (+0x%X): %s; tail %s" % (
    ext[V], in_v, "; ".join("%08X %s %s" % (a, i.mnemonic, i.op_str) for a, i in tail.items())))

# E4 class 19 (index 18): the arm loads LOW and HIGH before the shared tail
arm = vt[18]
seq = []
for i in md.disasm(at(arm, 0x60), arm):
    seq.append(i)
    if i.mnemonic == "jmp" or i.address >= 0x0032302E:
        break
imms = [i.operands[1].imm for i in seq if len(i.operands) == 2 and i.operands[1].type == X.X86_OP_IMM]
check("E4", 0xE000 in imms and 0xEFFF in imms, "class 19 arm %08X immediates %s -> admits [E000, EFFF) = E000..EFFE" % (
    arm, [hex(x) for x in imms]))

# E5
Q = 0x0031C5D0
qt = [BASE + u32(0x0031E598 + 4 * k) for k in range(32)]
qa = qt[11]
seq = []
for i in md.disasm(at(qa, 0x40), qa):
    seq.append(i)
    if i.mnemonic in ("jmp", "ret") or i.mnemonic.startswith("j"):
        break
reads_lane = any(("+ 4]" in i.op_str or "+ 6]" in i.op_str) for i in seq)
ret_m2 = any(i.op_str.endswith("0xfffffffe") for i in seq)
check("E5", ret_m2 and not reads_lane, "query table at 0031E598, class 12 arm %08X: %s" % (
    qa, "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in seq)))

# E6
def wrapper(f, rec, lane_off, lane_w):
    b = body(f)
    stores = [(rip_target(i, 0), i.operands[0].size) for i in b if i.operands and rip_target(i, 0)]
    calls = [i.operands[0].imm for i in b if i.mnemonic == "call" and i.operands[0].type == X.X86_OP_IMM]
    leas = [rip_target(i, 1) for i in b if i.mnemonic == "lea" and len(i.operands) == 2 and rip_target(i, 1)]
    zero98 = "0x98" in " ".join(i.op_str for i in b) or any(i.mnemonic.startswith("rep") for i in b) or \
        sum(1 for i in b if i.mnemonic in ("movups", "movaps", "movdqu", "mov") and i.operands and rip_target(i, 0)) >= 6
    ok = ((rec, 4) in stores and (rec + lane_off, lane_w) in stores and Q in calls and 0x0016D6A0 in calls and rec in leas)
    return ok, "stores %s; calls %s; lea record %s; clear-0x98 evidence %s" % (
        sorted("%08X/%d" % s for s in set(stores)), " ".join("%08X" % c for c in calls), rec in leas, zero98)


ok1, w1 = wrapper(0x0035D330, 0x022CA520, 4, 4)
ok2, w2 = wrapper(0x0035D380, 0x022CA480, 6, 2)
check("E6", ok1 and ok2, "0035D330: %s || 0035D380: %s" % (w1, w2))

# E7
b = body(0x0030B6A0)
ix = {i.address: k for k, i in enumerate(b)}
s = lambda a, n: ["%s %s" % (x.mnemonic, x.op_str) for x in b[ix[a]:ix[a] + n]]
clear = s(0x0030B702, 14)
mask = s(0x0030B739, 7)
r11_zero = any(x.mnemonic == "xor" and x.op_str == "r11d, r11d" for x in b if x.address < 0x0030B702)
# the clear: 8 passes of eight qword stores of r11 over 0x40 bytes = 0x200 bytes from state + 0x57C8
clear_ok = (clear[0] == "lea rax, [rcx + 0x57c8]" and clear[1] == "mov ecx, 8"
            and sum(1 for x in clear if x.startswith("mov qword ptr [rax") and x.endswith("r11")) == 8
            and "lea rax, [rax + 0x40]" in clear and clear[-1] == "jne 0x30b710")
mask_ok = (mask[0] == "lea rax, [r10 + 0x59c8]" and mask[1] == "mov ecx, 0x80"
           and "and byte ptr [rax], 0xf8" in mask and "lea rax, [rax + 1]" in mask)
check("E7", r11_zero and clear_ok and mask_ok,
      "0030B6A0: r11 zeroed %s; clear 8 x 0x40 from +0x57C8 %s (%s ... %s); mask 0x80 bytes from +0x59C8 with F8 %s" % (
          r11_zero, clear_ok, clear[0], clear[-1], mask_ok))

# E8
b = body(0x0020E600, 16)
b = b[:b.index(next(i for i in b if i.mnemonic == "ret")) + 1]
check("E8", len(b) == 3 and b[0].op_str == "eax, ecx" and b[1].mnemonic == "add" and rip_target(b[1], 1) == 0x01F83530,
      "0020E600: %s" % "; ".join("%s %s" % (i.mnemonic, i.op_str) for i in b))

# E9: the first record-lane read on each class's query arm, following the arm's straight line and its first jumps
WORD6 = {1, *range(5, 12), *range(13, 19), 30, 31}
DWORD4 = {2, 3, 4, *range(19, 30), 32}


def first_lane(a, depth=0, seen=None):
    seen = seen or set()
    if a in seen or depth > 6:
        return None
    seen.add(a)
    for i in md.disasm(at(a, 0x200), a):
        o = i.op_str
        if "word ptr [" in o and "+ 6]" in o and "rsp" not in o and "rip" not in o:
            return "WORD+6"
        if "dword ptr [" in o and "+ 4]" in o and "rsp" not in o and "rip" not in o and not o.startswith("dword ptr"):
            return "DWORD+4"
        if i.mnemonic == "ret":
            return None
        if i.mnemonic == "jmp":
            if i.operands[0].type == X.X86_OP_IMM:
                return first_lane(i.operands[0].imm, depth + 1, seen)
            return None
        if i.mnemonic.startswith("j") and i.operands[0].type == X.X86_OP_IMM:
            r = first_lane(i.operands[0].imm, depth + 1, seen)
            if r:
                return r
    return None


agree, disagree, none_found = [], [], []
for c in range(1, 33):
    got = first_lane(qt[c - 1])
    want = "WORD+6" if c in WORD6 else "DWORD+4" if c in DWORD4 else None
    if got is None:
        none_found.append(c)
    elif got == want:
        agree.append(c)
    else:
        disagree.append((c, got))
check("E9", not disagree, "first lane read agrees for %d classes %s; disagrees %s; no lane read found %s" % (
    len(agree), agree, disagree, none_found))

# E10: every rip-relative operand into the registry's span, image-wide
lo, hi = REG, REG + 15 * 0x58
fns = sorted(ext)
owner = {}
refs = []
import bisect  # noqa: E402
for f in fns:
    for i in md.disasm(at(f, ext[f]), f):
        for k in range(len(i.operands)):
            t = rip_target(i, k)
            if t is not None and lo <= t < hi:
                refs.append((f, i.address))
fn_set = sorted(set(f for f, _ in refs))
check("E10", set(fn_set) <= {0x0030B6A0, 0x0030B270},
      "rip-relative references into 01EEBCC0..%08X: %d in %d functions (%s)" % (
          hi, len(refs), len(fn_set), " ".join("%08X" % f for f in fn_set[:30])))

# E11: the conclusion E10's sentence supported - no code writes the offset qwords (+00/+18/+28). Every store through a
# pointer into the registry span, in all the functions E10 found, by the value-flow engine of k14_actorflow.py
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "k14-closure-stores-0930"))
import k14_actorflow as KF  # noqa: E402

span_stores = collections.defaultdict(set)


class RegStores(KF.Analysis):
    def summary(self, f, ctx, depth, stack):
        return (KF.UNK, ())

    def store(self, f, i, st, addr, size, val):
        if addr is not KF.UNK:
            for bb, o in addr:
                if isinstance(bb, str) and bb.startswith("G") and lo <= int(bb[1:], 16) < hi:
                    span_stores[f].add((i.address, "?" if o is None else (int(bb[1:], 16) + o - REG) % 0x58))
        return KF.Analysis.store(self, f, i, st, addr, size, val)


rs = RegStores()
for f in fn_set:
    rs.memo.clear()
    rs.run(f, {}, 0, (f,))
writers = sorted(span_stores)
fields = sorted(set(x for v in span_stores.values() for _, x in v), key=str)
offset_written = any(x in (0x00, 0x18, 0x28) for v in span_stores.values() for _, x in v)
known = {a for v in span_stores.values() for a, _ in v}
check("E11", writers == [0x0030B6A0] and not offset_written,
      "stores into the registry span: functions %s, fields %s, sites %s; offset qwords written: %s" % (
          " ".join("%08X" % f for f in writers), fields, " ".join("%08X" % a for a in sorted(known)), offset_written))

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
