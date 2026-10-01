"""Falsification pass 1 on CONTRACT-text-control-codes-and-dyngeo-draw (OPUS, 2026-09-29), from the shipping image.

Each check states its KILLER first; a claim survives only if the killer is absent.

  T0  §2 extents of the interpreter and the DynGeo bodies                                  KILLER: one differs
  T1  I-1 image-wide callers of 002AC5F0 are the seven cited sites, each `test eax, eax` / `je`   KILLER: another caller or shape
  T2  §3 the three tables tile 002AE334..002AE44D; all 50 targets inside the body; the two bounds; next function 002AE450
  T3  I-2 each parser's return on EVERY ret path                                           KILLER: a path returning otherwise
  T4  I-3 002ACFC2 is the only duplicate target, at 13 and 34; the case bytes cover 0..34; selectors '0' and '_'
  T5  I-4 002AC5F0 calls 002B2150 x7 and 002A9F00 x4, and each calls 002AC5F0 back
  T6  I-5 / I-8 the painter global, the terminator compare, and NUL and terminator sharing the exit 002AE31C
  T7  I-6 the escape advances the cursor past 0x0F only; out of range returns 1 with the cursor on the selector
  T8  I-7 the entry clear of the advance pair and *out2
  T9  I-9 two tail jumps into 002142A0; none from 002143E0; ShadowFinal's primitive 3
  T10 I-10 the sixteen floats of the axis pool
  T11 I-11 slot 11: +0x118 tail jumps; the third-argument forms
  T12 I-12 the ten-layer walk anchors, the 480 clamp, the 48-byte stride
  T13 I-13 the three destructors stamp 00906DE8 and free 0x160 / 0x170 / 0x168
  T14 §3 the four vtables: stride 0x68, slot columns, eight identical slots, slot 0 = a 3-byte `ret 0`; 00906DC8 has 3 slots
  T15 §5/§6 construction: six references into the vtable window, constructors called only from 001E8580, sizes, one pointer per slot-10 body
  T16 §7 / §10.1 against I-6's correction: an out-of-range selector is NOT consumed                KILLER: a cursor write after 002AD01D on that path
"""
import bisect, collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try: sizes[int(p[0], 16)] = int(p[2])
        except ValueError: pass
FN = sorted(sizes)
_c = {}
def body(a):
    if a not in _c:
        _c[a] = list(md.disasm(blob[OFF(a):OFF(a) + sizes[a]], a))
    return _c[a]
def at(a, fn=None):
    for x in (body(fn) if fn else []):
        if x.address == a:
            return x
    return next(md.disasm(blob[OFF(a):OFF(a) + 16], a))
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
S = lambda x: "%s %s" % (x.mnemonic, x.op_str)
def owner(a):
    k = bisect.bisect_right(FN, a) - 1
    return FN[k] if k >= 0 and FN[k] <= a < FN[k] + sizes[FN[k]] else None

I, END = 0x002AC5F0, 0x002AC5F0 + 7489
ib = body(I); ix = {x.address: k for k, x in enumerate(ib)}

# T0
want0 = {0x002AC5F0: 7489, 0x002142A0: 306, 0x00214210: 139, 0x00214540: 82, 0x002143E0: 352, 0x00214890: 24, 0x002148B0: 33}
d0 = {("%08X" % k): sizes.get(k) for k, v in want0.items() if sizes.get(k) != v}
check("T0", not d0, "extent mismatches %s" % (d0 or "none"))

# whole-image direct-call and rip-reference sweep (per listed body; a linear .text sweep stops at bad bytes)
text = next(x for x in SECS if x[0] == ".text")
calls_to = collections.defaultdict(list); riprefs = collections.defaultdict(list)
for fa in FN:
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    for x in md.disasm(code, fa):
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))
        for t in rip(x):
            if 0x00906DE8 <= t <= 0x00906F88:        # the page's four-vtable window
                riprefs[t].append((fa, x.address, S(x)))

# T1
sites = [(f, a) for f, a, m in calls_to[I] if m == "call" and f != I]
shape = {}
for f, a in sites:
    nxt = [S(y) for y in md.disasm(blob[OFF(a):OFF(a) + 24], a)][:3]
    shape["%08X" % a] = nxt[1:3]
want1 = {0x002A8C50: 0x002A9726, 0x002A9F00: 0x002AA6A8, 0x002AAE40: 0x002AB5B0, 0x002AF340: 0x002AF783, 0x002B1FB0: 0x002B207E,
         0x002B2150: 0x002B2393, 0x002B5730: 0x002B5823}
# CORRECTED (pass 1): five callers loop on the return; 002B1FB0 and 002B5730 call once, DISCARD eax, and read the cursor
# delta ([rsp+0x28] - start) as a code length - they depend on the cursor side effect, not the loop protocol
loopers = sorted(a for a, v in shape.items() if v[0] == "test eax, eax" and v[1].startswith("je "))
probes = sorted(a for a, v in shape.items() if v[0].endswith("dword ptr [rsp + 0x28]") and v[1].startswith("sub "))
ok1 = sorted(sites) == sorted(want1.items()) and loopers == ["002A9726", "002AA6A8", "002AB5B0", "002AF783", "002B2393"] and probes == ["002B207E", "002B5823"]
check("T1", ok1, "callers %s; loop on the return at %s; single-shot length probes (return discarded, cursor delta read) at %s" % (
    ["%08X@%08X" % s_ for s_ in sorted(sites)], loopers, probes))

# T2
tok = [struct.unpack_from("<I", blob, OFF(0x002AE334) + 4 * i)[0] + BASE for i in range(15)]
esc = [struct.unpack_from("<I", blob, OFF(0x002AE370) + 4 * i)[0] + BASE for i in range(35)]
case = list(blob[OFF(0x002AE3FC):OFF(0x002AE3FC) + 0x51])
inside = all(I <= t < END for t in tok + esc)
last = ib[-1]
check("T2", inside and S(at(0x002AC694, I)) == "cmp eax, 0xe" and S(at(0x002AD026, I)) == "cmp eax, 0x50" and last.address == 0x002AE32C
      and 0x002AE3FC + 0x51 == 0x002AE44D and 0x002AE450 in sizes,
      "all 50 targets inside: %s; 002AC694 `%s`; 002AD026 `%s`; last instruction %08X `%s`; next function 002AE450 listed: %s" % (
          inside, S(at(0x002AC694, I)), S(at(0x002AD026, I)), last.address, S(last), 0x002AE450 in sizes))

# T3
def rets(fa):
    """(ret address, the last write to eax/rax before it in the same straight line) for every ret"""
    b = body(fa); out = []
    for k, x in enumerate(b):
        if x.mnemonic == "ret":
            w = next((S(y) for y in reversed(b[max(0, k - 12):k]) if y.op_str.split(",")[0].strip() in ("eax", "rax")), None)
            out.append(("%08X" % x.address, w))
    return out
PARSERS = (0x003FFAB0, 0x003FFB00, 0x003FFB90, 0x003FFBC0, 0x003FFC60, 0x003FFCE0, 0x003FFD70, 0x003FFDA0, 0x003FFDF0, 0x003FFEE0, 0x003FFF10)
r3 = {("%08X" % p_): rets(p_) for p_ in PARSERS}
const = lambda p_, v: r3["%08X" % p_] and all(w == "mov eax, %d" % v for _a, w in r3["%08X" % p_])
ok3 = (all(const(p_, 3) for p_ in (0x003FFAB0, 0x003FFB90, 0x003FFC60, 0x003FFDA0, 0x003FFEE0)) and all(const(p_, 4) for p_ in (0x003FFCE0, 0x003FFF10)))
check("T3", ok3, "returns per ret path: %s" % r3)

# T4
cnt = collections.Counter(esc)
dups = {("%08X" % t): [i for i, e in enumerate(esc) if e == t] for t, n in cnt.items() if n > 1}
sel = {chr(0x20 + i): v for i, v in enumerate(case)}
check("T4", dups == {"002ACFC2": [13, 34]} and sorted(set(case)) == list(range(35)) and sel["0"] == 13 and sel["_"] == 34,
      "duplicate targets %s; case values distinct %d covering 0..34: %s; '0' -> %d, '_' -> %d" % (
          dups, len(set(case)), sorted(set(case)) == list(range(35)), sel["0"], sel["_"]))

# T5
c7 = sum(1 for x in ib if x.mnemonic == "call" and T(x) == 0x002B2150); c4 = sum(1 for x in ib if x.mnemonic == "call" and T(x) == 0x002A9F00)
back = [f for f, a, m in calls_to[I] if f in (0x002B2150, 0x002A9F00)]
check("T5", c7 == 7 and c4 == 4 and sorted(set(back)) == [0x002A9F00, 0x002B2150], "002B2150 x%d, 002A9F00 x%d; they call back: %s" % (
    c7, c4, sorted("%08X" % b for b in set(back))))

# T6
p650 = at(0x002AC650, I); c666 = at(0x002AC666, I); j = ib[ix[0x002AC666] + 1]
nul = [x for x in ib if 0x002AC640 <= x.address <= 0x002AC650 and x.mnemonic == "je"]
check("T6", rip(p650) == [0x0209CC40] and S(c666) == "cmp ax, word ptr [rcx]" and j.mnemonic == "je" and T(j) == 0x002AE31C and nul and T(nul[0]) == 0x002AE31C,
      "002AC650 `%s`; 002AC666 `%s` / `%s`; NUL test jumps to %s" % (S(p650), S(c666), S(j), ["%08X" % T(n) for n in nul]))

# T7 / T16
e = [S(x) for x in ib if 0x002AD01A <= x.address <= 0x002AD029]
fin = [S(x) for x in ib if 0x002ACFC2 <= x.address <= 0x002ACFD0]
post = [x for x in ib if 0x002AD01D < x.address <= 0x002AD029 and x.op_str.startswith("qword ptr [rdi]")]
check("T7", "inc rcx" in e and "mov qword ptr [rdi], rcx" in e and "ja 0x2acfc2" in e and fin and fin[0] == "mov eax, 1",
      "escape 002AD01A..029 %s; exit 002ACFC2 %s" % (e, fin[:3]))
exit_writes = [x for x in ib if 0x002ACFC2 <= x.address <= 0x002ACFD0 and x.op_str.startswith("qword ptr [rdi]")]
check("T16", not post and not exit_writes, "cursor writes after 002AD01D on the out-of-range path: %d, at the exit: %d - the selector is not consumed, so §7's "
      "'consumed anyway' and §10.1's 'consumed and skipped' contradict I-6's correction" % (len(post), len(exit_writes)))

# T8
e8 = {a: S(at(a, I)) for a in (0x002AC61B, 0x002AC628, 0x002AC62E, 0x002AC638)}
check("T8", e8[0x002AC61B] == "xor eax, eax" and "r9]" in e8[0x002AC628] and rip(at(0x002AC62E, I)) == [0x0209CC60] and rip(at(0x002AC638, I)) == [0x0209CC68],
      "%s" % {("%08X" % k): v for k, v in e8.items()})

# T9
sf = body(0x002143E0)
to_base = [S(x) for x in sf if x.mnemonic in ("call", "jmp") and T(x) == 0x002142A0]
check("T9", T(at(0x00214296, 0x00214210)) == 0x002142A0 and at(0x00214296, 0x00214210).mnemonic == "jmp" and T(at(0x0021458D, 0x00214540)) == 0x002142A0
      and not to_base and S(at(0x00214520, 0x002143E0)) == "mov edx, 3", "Final 00214296 `%s`; Shadow 0021458D `%s`; ShadowFinal edges to the base %s; 00214520 `%s`" % (
          S(at(0x00214296, 0x00214210)), S(at(0x0021458D, 0x00214540)), to_base or "none", S(at(0x00214520, 0x002143E0))))

# T10
pool = {a: struct.unpack_from("<4f", blob, OFF(a)) for a in range(0x008C5F80, 0x008C5FE0, 0x10)}
want10 = {0x008C5F80: (1, 0, 0, 0), 0x008C5F90: (0, 1, 0, 0), 0x008C5FA0: (0, -1, 0, 0), 0x008C5FB0: (0, 0, 1, 0), 0x008C5FC0: (0, 0, -1, 0), 0x008C5FD0: (0, 0, 0, 1)}
check("T10", all(pool[k] == v for k, v in want10.items()), "pool %s" % {("%08X" % k): v for k, v in pool.items()})

# T11
s11 = {h: [S(x) for x in body(h)] for h in (0x00214890, 0x002148B0, 0x00214860)}
check("T11", all(any("0x118" in t and t.startswith("jmp") for t in v) for v in s11.values()) and "xor r8d, r8d" in s11[0x00214890]
      and any(t.startswith("neg") for t in s11[0x00214860]) and any(t.startswith("sbb") for t in s11[0x00214860]),
      "%s" % {("%08X" % k): v for k, v in s11.items()})

# T12
b12 = {a: S(at(a, 0x002142A0)) for a in (0x002142B4, 0x002142BA, 0x002142C9, 0x002142D6, 0x0021432D, 0x00214332, 0x00214338, 0x0021433A, 0x00214356, 0x0021435D)}
check("T12", b12[0x002142B4] == "mov r12d, 0xa" and "0xa8" in b12[0x002142BA] and "+ 8]" in b12[0x002142C9] and b12[0x002142D6] == "je 0x2143a0"
      and b12[0x0021433A] == "mov r12d, 0x1e0" and b12[0x00214356] == "lea r8, [rcx + rcx*2]" and b12[0x0021435D] == "shl r8, 4",
      "%s" % {("%08X" % k): v for k, v in b12.items()})

# T13
d13 = {}
for h in (0x00213AD0, 0x00213AA0, 0x00213B00):
    b = body(h)
    d13["%08X" % h] = ([("%08X" % t) for x in b for t in rip(x)], [x.op_str for x in b if x.mnemonic == "mov" and x.op_str.startswith("edx, 0x1")])
check("T13", all(v[0] == ["00906DE8"] for v in d13.values()) and [v[1] for v in d13.values()] == [["edx, 0x160"], ["edx, 0x170"], ["edx, 0x168"]],
      "%s" % d13)

# T14
vt = {}
for b in (0x00906DE8, 0x00906E50, 0x00906EB8, 0x00906F20):
    vt[b] = [struct.unpack_from("<Q", blob, OFF(b + 8 * k))[0] for k in range(12)]
rtti = [struct.unpack_from("<Q", blob, OFF(b - 8))[0] for b in vt]
cols = {k: [vt[b][k] for b in vt] for k in range(12)}
diff_cols = sorted(k for k, v in cols.items() if len(set(v)) > 1)
want14 = {2: [0x00213AD0, 0x00213B00, 0x00213AA0, 0x00213B00], 6: [0x00213D10, 0x00213D10, 0x00213B40, 0x00213D10],
          10: [0x002142A0, 0x00214540, 0x00214210, 0x002143E0], 11: [0x00214890, 0x002148B0, 0x00214860, 0x00214860]}
ret0 = blob[OFF(0x0016D6A0):OFF(0x0016D6A0) + 3] == b"\xc2\x00\x00"
base3 = [struct.unpack_from("<Q", blob, OFF(0x00906DC8 + 8 * k))[0] for k in range(3)]
check("T14", diff_cols == [2, 6, 10, 11] and all(cols[k] == v for k, v in want14.items()) and all(v[0] == 0x0016D6A0 for v in vt.values()) and ret0
      and base3 == [0x0016D6A0, 0x00213140, 0x00213110] and all(r_ != 0 for r_ in rtti),
      "stride 0x68; differing slots %s; slot 0 all 0016D6A0 (`ret 0`: %s); 00906DC8 %s; RTTI locators present %s" % (
          diff_cols, ret0, ["%08X" % x for x in base3], all(r_ != 0 for r_ in rtti)))

# T15
refs = sorted((f, a) for t, lst in riprefs.items() for f, a, _s in lst)
ctors = {0x002138C0: "Final", 0x00213960: "ShadowFinal", 0x00213A00: "Shadow"}
ccalls = {("%08X" % c): sorted("%08X" % a for f, a, m in calls_to[c] if m == "call") for c in ctors}
sz = {}
for c in ctors:
    for f, a, m in calls_to[c]:
        pre = list(md.disasm(blob[OFF(a) - 0x40:OFF(a)], a - 0x40))
        sz["%08X" % a] = [x.op_str for x in pre if x.op_str.startswith("edx, 0x1")][-1:]
flushers = sorted(set("%08X" % f for f, a, m in calls_to[0x001E8580] if m == "call"))
wrap = calls_to[0x0017F850]
ptrs = {}
for b in (0x002142A0, 0x00214540, 0x00214210, 0x002143E0):
    pat = struct.pack("<Q", b)
    ptrs["%08X" % b] = sum(len(re.findall(re.escape(pat), blob[raw:raw + rsz])) for _n, _s, _z, raw, rsz in SECS)
check("T15", len(refs) == 6 and all(0x00213000 <= f < 0x00214000 for f, a in refs)
      and ccalls == {"002138C0": ["001E8F84"], "00213960": ["001E8A7D"], "00213A00": ["001E86BB", "001E88C4"]}
      and flushers == ["0017F850"] and len([w for w in wrap if w[2] == "call"]) == 12 and len({w[0] for w in wrap if w[2] == "call"}) == 8
      and all(v == 1 for v in ptrs.values()),
      "vtable-window references %d, owners %s; constructor call sites %s; sizes before them %s; flush callers %s; 0017F850 %d call sites in %d functions; "
      "8-byte pointers per slot-10 body %s" % (len(refs), sorted(set("%08X" % f for f, a in refs)), ccalls, sz, flushers,
                                              len([w for w in wrap if w[2] == "call"]), len({w[0] for w in wrap if w[2] == "call"}), ptrs))

print("BROKEN %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
