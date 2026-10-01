"""sd61_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for SD-61 (2026-09-30). Read-only on the image.
Branch census by raw E8/E9/0F8x sweep of .text (not the function list). For each call site of the PAnnotation
constructor 006B66C0, follows the annotation object A (rcx) through the site and checks, per site, what the author's
checker assumes but does not test: r8 is 00630180's return, the 0x7FFFFFFF store lands on A+0x30, the derived vtable
lands on A+0, and the later 006B67D0 attach links A into (the 00632960 member M)+0x38 of the SAME registration."""
import sys, struct, collections, re
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk

CTOR, MEMBER, ATTACH, TYPEGET = 0x006B66C0, 0x00632960, 0x006B67D0, 0x00630180
blob = tk.d[tk.TRO:tk.TRO + tk.TRS]
sites = collections.defaultdict(list)
for i in range(len(blob) - 6):
    b = blob[i]
    if b in (0xE8, 0xE9):
        t = tk.TVA + i + 5 + struct.unpack_from("<i", blob, i + 1)[0]
        if t == CTOR: sites["E8" if b == 0xE8 else "E9"].append(tk.TVA + i)
    elif b == 0x0F and 0x80 <= blob[i + 1] <= 0x8F:
        t = tk.TVA + i + 6 + struct.unpack_from("<i", blob, i + 2)[0]
        if t == CTOR: sites["jcc"].append(tk.TVA + i)
print("raw branches to 006B66C0:", {k: len(v) for k, v in sites.items()})

def ripT(x, k=1):
    op = x.operands[k]
    return x.address + x.size + op.mem.disp if op.type == tk.X86_OP_MEM and x.reg_name(op.mem.base) == "rip" else None

def cstr(a):
    o = tk.off(a); e = tk.d.index(b"\0", o); return tk.d[o:e].decode("latin-1")

res = collections.Counter(); odd = []; members = set(); owners = set()
for a in sites["E8"]:
    o, how = tk.owner(a)
    xs = tk.dis(o, a + 0x200)
    k = next(j for j, x in enumerate(xs) if x.address == a)
    pre, post = xs[max(0, k - 12):k], xs[k + 1:k + 60]
    A = next((ripT(x) for x in reversed(pre) if x.mnemonic == "lea" and x.op_str.startswith("rcx, [rip")), None)
    key = next((ripT(x) for x in reversed(pre) if x.mnemonic == "lea" and x.op_str.startswith("rdx, [rip")), None)
    r8ok = any(x.op_str == "r8, rax" for x in pre) and any(x.mnemonic == "call" and x.op_str == hex(TYPEGET) for x in pre)
    r9zero = any(x.mnemonic == "xor" and x.op_str == "r9d, r9d" for x in pre)
    # member registration: last call 00632960 in the 120 instructions before, its rcx lea and r9 (name) lea
    back = xs[max(0, k - 120):k]
    j = max((i for i, x in enumerate(back) if x.mnemonic == "call" and x.op_str == hex(MEMBER)), default=None)
    M = nm = None
    if j is not None:
        M = next((ripT(x) for x in reversed(back[max(0, j - 12):j]) if x.mnemonic == "lea" and x.op_str.startswith("rcx, [rip")), None)
        n = next((ripT(x) for x in reversed(back[max(0, j - 12):j]) if x.mnemonic == "lea" and x.op_str.startswith("r9, [rip")), None)
        nm = cstr(n) if n else None
    v30 = any(x.mnemonic == "mov" and ripT(x, 0) == (A or 0) + 0x30 and x.op_str.endswith("0x7fffffff") for x in post[:6])
    vt0 = any(x.mnemonic == "mov" and ripT(x, 0) == A for x in post[:6])
    att = None
    for i2, x in enumerate(post):
        if x.mnemonic == "call" and x.op_str == hex(ATTACH):
            rc = next((ripT(y) for y in reversed(post[max(0, i2 - 4):i2]) if y.mnemonic == "lea" and y.op_str.startswith("rcx, [rip")), None)
            rd = next((ripT(y) for y in reversed(post[max(0, i2 - 4):i2]) if y.mnemonic == "lea" and y.op_str.startswith("rdx, [rip")), None)
            att = (rc, rd); break
    attok = att is not None and M is not None and att == (M + 0x38, A)
    row = ("%08X" % key if key else "nonrip", r8ok, r9zero, nm, v30, vt0, attok)
    res[row] += 1
    if M: members.add(M); owners.add(o)
    if row[0] != "02CF8570": odd.append("%08X in %s: %r" % (a, tk.fname(a), row))
print("per-site (key, r8=00630180 ret, r9d=0, member name, [A+0x30]=0x7FFFFFFF, [A]=vtable, attach(M+0x38, A)) :")
for r, n in res.most_common(): print("  %2d x %r" % (n, r))
for s in odd: print("  odd:", s)
print("distinct member objects M: %d, distinct owning functions: %d" % (len(members), len(owners)))
wm = tk.u64(0x02CF8570)
print("key object 02CF8570 file qword:", "None (virtual tail, runtime-built)" if wm is None else hex(wm))
