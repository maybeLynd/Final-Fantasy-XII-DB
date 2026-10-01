"""res_request_census.py: every direct call to the resource request API with a constant (kind, id), resolved to the
file name through the path directory 0215F000[kind] as 002DF9A0 fills it for its first language arm.
API conventions: pool family (rcx = pool, edx = kind, r8d = id): 00249210, 002493D0, 00249350, 00249180;
path family (ecx = kind, edx = id): 0032E400 (size), 0032E620 (request), 0032E3F0.
Constants are tracked linearly inside the calling function from the start of its body to the call: mov r32/r64, imm;
xor r, r; lea r, [r' + imm] with r' known; a call clears the volatile registers. Sites whose kind or id is not a
constant are reported as such (register-held values are exactly the part this census cannot see).
Usage (needs the raw call index tools/rawcalls.json, so run from Database/Tools/work/FABLE/pub140-scratch):
    python <this file> > constant-resource-requests.tsv"""
import json, re, struct, bisect, collections, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_REG, X86_OP_MEM
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [(struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 12)[0], struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 8)[0],
         struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 20)[0], struct.unpack_from("<I", d, pe + 24 + opt + i * 40 + 16)[0]) for i in range(ns)]
def off(va):
    r = va - BASE
    for a, vs, ro, rs in secs:
        if a <= r < a + min(vs, rs): return ro + r - a
def q(va):
    o = off(va); return struct.unpack_from("<Q", d, o)[0] if o is not None else None
def cstr(va):
    o = off(va)
    if o is None: return None
    s = d[o:d.index(b"\0", o)]
    return s.decode("latin1") if s and all(32 <= c < 127 for c in s) else None
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError): pass
ks = sorted(sizes)
def own(s):
    i = bisect.bisect_right(ks, s) - 1
    return ks[i] if i >= 0 and ks[i] <= s < ks[i] + sizes[ks[i]] else None
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
def body(f):
    o = off(f); return list(md.disasm(d[o:o + sizes[f]], f))
# the directory: 002DF9A0's writes (first write per slot kept, i.e. the first language arm in address order) of `lea rax, [rip+X]; mov [rip+0215F000+8k], rax`
kinds = {}
last = {}
for ins in body(0x2DF9A0):
    m = re.match(r"(r[a-z0-9]+), \[rip [+-] 0x[0-9a-f]+\]$", ins.op_str)
    if ins.mnemonic == "lea" and m:
        last[m.group(1)] = ins.address + ins.size + ins.operands[1].mem.disp
    elif ins.mnemonic == "mov" and ins.op_str.startswith("qword ptr [rip"):
        reg = ins.op_str.rsplit(", ", 1)[1]
        dst = ins.address + ins.size + ins.operands[0].mem.disp
        if reg in last and 0x215F000 <= dst < 0x215F200 and (dst - 0x215F000) % 8 == 0:
            kinds.setdefault((dst - 0x215F000) // 8, last[reg])
    elif ins.mnemonic == "ret": break
POOL = {0x249210, 0x2493D0, 0x249350, 0x249180}
PATH = {0x32E400, 0x32E620, 0x32E3F0}
raw = json.load(open("tools/rawcalls.json"))
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
C32 = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "r8d": "r8", "r9d": "r9", "r10d": "r10", "r11d": "r11",
       "r12d": "r12", "r13d": "r13", "r14d": "r14", "r15d": "r15", "r8w": "r8", "dx": "rdx", "cx": "rcx"}
def canon(r): return C32.get(r, r)
ARGREG = ("rcx", "rdx", "r8", "r9")
def track(f, s, seed_args):
    """register values at call site s in f: ints for constants, ("arg", n) for an untouched entry argument."""
    val = {r: ("arg", n) for n, r in enumerate(ARGREG)} if seed_args else {}
    for ins in body(f):
        if ins.address >= s: break
        ops = ins.operands
        if ins.mnemonic == "call":
            for r in VOL: val.pop(r, None)
            continue
        if len(ops) == 2 and ops[0].type == X86_OP_REG:
            dst = canon(ins.reg_name(ops[0].reg))
            if ins.mnemonic == "mov" and ops[1].type == X86_OP_IMM: val[dst] = ops[1].imm & 0xFFFFFFFF
            elif ins.mnemonic == "xor" and ops[1].type == X86_OP_REG and ops[1].reg == ops[0].reg: val[dst] = 0
            elif ins.mnemonic == "lea" and ops[1].type == X86_OP_MEM and ops[1].mem.base and not ops[1].mem.index:
                b = canon(ins.reg_name(ops[1].mem.base))
                if b in val and isinstance(val[b], int): val[dst] = (val[b] + ops[1].mem.disp) & 0xFFFFFFFF
                elif b in val and ops[1].mem.disp == 0: val[dst] = val[b]
                else: val.pop(dst, None)
            elif ins.mnemonic in ("mov", "movsxd", "movzx") and ops[1].type == X86_OP_REG:
                sr = canon(ins.reg_name(ops[1].reg))
                if sr in val: val[dst] = val[sr]
                else: val.pop(dst, None)
            elif ins.mnemonic not in ("cmp", "test"): val.pop(dst, None)
    return val
out = []   # (api, site, function, kind, id, via caller site or None)
hop = collections.Counter()
for tgt in sorted(POOL | PATH):
    sites = sorted(set(int(s, 16) for s in raw.get("%X" % tgt, [])))
    for s in sites:
        f = own(s)
        if f is None: out.append((tgt, s, None, None, None, None)); continue
        val = track(f, s, True)
        kreg, ireg = ("rdx", "r8") if tgt in POOL else ("rcx", "rdx")
        k, i = val.get(kreg), val.get(ireg)
        if isinstance(k, int) and isinstance(i, int) or k is None or i is None:
            out.append((tgt, s, f, k if isinstance(k, int) else None, i if isinstance(i, int) else None, None)); continue
        # one hop: kind and/or id still hold the function's own entry arguments at the call
        got = False
        for cs in sorted(set(int(x, 16) for x in raw.get("%X" % f, []))):
            cf = own(cs)
            if cf is None: continue
            cv = track(cf, cs, False)
            kk = cv.get(ARGREG[k[1]]) if isinstance(k, tuple) else k
            ii = cv.get(ARGREG[i[1]]) if isinstance(i, tuple) else i
            if isinstance(kk, int) and isinstance(ii, int):
                out.append((tgt, s, f, kk, ii, cs)); got = True; hop["resolved at a caller"] += 1
        if not got:
            out.append((tgt, s, f, None, None, None)); hop["argument-held, no constant caller"] += 1
print("api\tsite\tfunction\tname\tkind\tid\tfile\tvia_caller_site")
cnt = collections.Counter()
for tgt, s, f, k, i, via in out:
    fn = None
    if k is not None and i is not None and k in kinds:
        p = q(kinds[k] + 8 * i)
        fn = cstr(p) if p else None
    cnt["resolved" if fn else ("const-unresolved" if k is not None and i is not None else "register-held")] += 1
    print("%08X\t%08X\t%s\t%s\t%s\t%s\t%s\t%s" % (tgt, s, "%08X" % f if f else "-", names.get(f, "-") if f else "-",
          "-" if k is None else hex(k), "-" if i is None else hex(i), fn or "-", "%08X" % via if via else "-"))
print("# rows", len(out), dict(cnt), "one-hop", dict(hop), "kinds in directory", len(kinds), file=sys.stderr)
