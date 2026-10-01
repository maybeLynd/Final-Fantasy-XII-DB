"""DD residue batch 6 (SWE2-CONTRACT, 2026-09-30): static checks behind the request-queue page's reconciled residue.

Page: 02-Resource-And-Asset-Pipeline/the-resource-request-queue.md. Image: the certified shipping EXE (asserted).
Run: python -B b6_request_queue.py  (exit 0 and FAILS 0 expected)

  A1-A6  the six asking-form callers the page called unread pass 1 (the non-draining ask) and act only on "idle"
  M1     the request pool 022C31C0..022C51D8 is rip-referenced only by queue-module functions (0032E000..0032ED00)
  M2     no .text instruction addresses the pool image-base-relatively (disp32 = RVA); control: the pump's jump table
  G1     the 16-byte gap 022C51E0..022C51EF before the size overrides: two stores of 0, no reader
  Z1     every qword access at displacement 0 in the module, classified: slot +0 is written by 0032E153 (add),
         0032E229, 0032E725 and 0032E97C (0) and read by nothing else
  Z2     slot +0x50 (the part callback) is stored only as 0 (0032E6FF with r14 = 0, 0032E959) and read at 0032E3B4
  Z3     every indirect call in the module and the argument it passes: only the part callback receives a slot pointer
"""
import hashlib, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "Tools", "analysis-kit", "gfz-scripts"))
import retool as T  # noqa: E402

FAILS = 0
RIP = 41
LO, HI = 0x0032E000, 0x0032ED00
BASE = 0x00120000


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(a):
    return next(T.R.md.disasm(T.R.at(a, 16), a, 1))


def txt(i):
    return "%s %s" % (i.mnemonic, i.op_str)


def pin(name, a, text):
    i = ins(a)
    check(name, text in txt(i), "%08X  %s" % (a, txt(i)))


sha = hashlib.sha256(open(T.R.b.EXE, "rb").read()).hexdigest()
print("image", sha)
check("image identity", sha == "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8")
SZ = T.sizes()
MOD = sorted(f for f in SZ if LO <= f < HI)


def body(f):
    return list(T.R.md.disasm(T.R.at(f, SZ[f]), f))


# ---- A: the six asking-form sites
for tag, gate, lea_, call_ in (("A1 002FC3C0", 0x002FC403, 0x002FC405, 0x002FC408),
                               ("A2 003B1310", 0x003B138D, 0x003B138F, 0x003B1392),
                               ("A3 003B1710", 0x003B179B, 0x003B179D, 0x003B17A0),
                               ("A4 003B18E0", 0x003B197C, 0x003B197E, 0x003B1981)):
    pin(tag + " in-flight test (0032E4D0) nonzero skips", gate, "jne")
    pin(tag + " so eax is 0 here: ecx = 1", lea_, "lea ecx, [rax + 1]")
    pin(tag + " the ask", call_, "call 0x32e520")
pin("A1 idle: clears 02EC3D7C", 0x002FC411, "mov byte ptr [rip + 0x2bc7964], 0")
for a in (0x003B139E, 0x003B17AC, 0x003B198D):
    pin("A2-A4 idle: 003B21E0(obj)", a, "call 0x3b21e0")
pin("A5 0034DB30 edi = 1", 0x0034DB49, "mov edi, 1")
pin("A5 ecx = edi", 0x0034DBD7, "mov ecx, edi")
pin("A5 the ask", 0x0034DBD9, "call 0x32e520")
w5 = [i for i in body(0x0034DB30) if 0x0034DB49 < i.address < 0x0034DBD7 and re.match(r"(e|r)di\b", i.op_str)
      and i.mnemonic not in ("cmp", "test")]
def returns_soon(f, a):
    seq = body(f)
    k = next(j for j, x in enumerate(seq) if x.address == a)
    for x in seq[k + 1:k + 9]:
        if x.mnemonic == "ret":
            return True
        if x.mnemonic.startswith("j") or x.mnemonic == "call":
            return False
    return False


check("A5 every other edi write lies on a path that returns before the ask", all(returns_soon(0x0034DB30, i.address) for i in w5),
      str([("%08X" % i.address, txt(i)) for i in w5]))
pin("A5 ...and that path returns", 0x0034DBAB, "ret")
pin("A6 0050D0C0 ebx = 1", 0x0050D0D2, "mov ebx, 1")
pin("A6 ecx = ebx", 0x0050D12F, "mov ecx, ebx")
pin("A6 the ask", 0x0050D131, "call 0x32e520")
w6 = [i for i in body(0x0050D0C0) if 0x0050D0D2 < i.address < 0x0050D12F and re.match(r"(e|r)bx\b", i.op_str)
      and i.mnemonic not in ("cmp", "test")]
check("A6 every other ebx write lies on a path that returns before the ask", all(returns_soon(0x0050D0C0, i.address) for i in w6),
      str([("%08X" % i.address, txt(i)) for i in w6]))
pin("A6 busy: 00314D40(1)", 0x0050D13C, "call 0x314d40")
pin("A0 the ask returns without pumping when ecx != 0", 0x0032E526, "je 0x32e561")

# ---- M: who can hold a slot pointer
refs = T.scan()["refs"]
users = sorted({f for g in refs if 0x022C31C0 <= g < 0x022C51D8 for f, _, _ in refs[g]})
check("M1 pool rip-referencers are module functions", users and all(LO <= f < HI for f in users),
      str(["%08X" % f for f in users]))
raw = open(T.R.b.EXE, "rb").read()
pe_off = struct.unpack_from("<I", raw, 0x3C)[0]
nsec = struct.unpack_from("<H", raw, pe_off + 6)[0]
opt = struct.unpack_from("<H", raw, pe_off + 20)[0]
sec0 = pe_off + 24 + opt
secs = [struct.unpack_from("<8sIIII", raw, sec0 + 40 * k) for k in range(nsec)]
name, vsize, va, rsize, roff = [x for x in secs if x[0].rstrip(bytes(1)) == b".text"][0]
blob = raw[roff:roff + rsize]


class _T:
    VirtualAddress = va


t = _T
lo_r, hi_r = 0x022C31C0 - BASE, 0x022C51F0 - BASE   # pool, list record and the 16-byte gap
hits = [BASE + t.VirtualAddress + o for o in range(len(blob) - 3)
        if lo_r <= struct.unpack_from("<I", blob, o)[0] < hi_r]
ctrl = [BASE + t.VirtualAddress + o for o in range(len(blob) - 3)
        if struct.unpack_from("<I", blob, o)[0] == 0x0032E2D0 - BASE]
check("M2 control: the pump's jump-table RVA 0x20E2D0 is found", any(0x0032E0B1 <= a < 0x0032E0B8 for a in ctrl),
      str(["%08X" % a for a in ctrl]))
def as_disp(a):
    """is the dword at a the displacement of a decoded instruction in its function?"""
    f = T.func_of(a, SZ)
    if f is None:
        return "no function"
    for i in body(f):
        if i.address <= a < i.address + i.size:
            for op in i.operands:
                if op.type == 3 and (op.mem.disp & 0xFFFFFFFF) == struct.unpack_from("<I", raw, roff + a - BASE - va)[0]:
                    return txt(i)
            return None
    return None


real = [(a, as_disp(a)) for a in hits]
print("   raw dword hits:", [("%08X" % a, d) for a, d in real])
check("M2 no instruction displacement equals a pool RVA", not [a for a, d in real if d], str(real))
check("M2 control: the pump's jump-table RVA decodes as a displacement", any(as_disp(a) for a in ctrl), str([as_disp(a) for a in ctrl]))

# ---- G1: the 16 bytes between the list record and the size overrides (022C51E0..022C51EF)
g = sorted((a, f, k) for x in refs if 0x022C51E0 <= x < 0x022C51F0 for f, a, k in refs[x])
check("G1 the gap is referenced only by two stores of 0", [(a, k) for a, f, k in g] == [(0x0032EAA7, "W"), (0x0032EAE0, "W")],
      str([("%08X" % a, "%08X" % f, k) for a, f, k in g]))
pin("G1 0032EAA7 stores rdx = 0", 0x0032EA9E, "xor edx, edx")
pin("G1 0032EAE0 stores 0", 0x0032EAE0, "mov qword ptr [rip + 0x1f966f5], 0")

# ---- Z1: displacement-0 qword accesses in the module
EXPECT_SLOT0 = {0x0032E153: "add qword ptr [rbx], rax", 0x0032E229: "mov qword ptr [rbx], 0",
                0x0032E725: "mov qword ptr [rcx], r14", 0x0032E97C: "mov qword ptr [r10], 0"}
EXPECT_OTHER = {0x0032E47A: "biased init cursor (pool + 0x18): slot +0x18",
                0x0032EAB1: "the 022C51F0 array, not the pool"}
seen = {}
for f in MOD:
    for i in body(f):
        for op in i.operands:
            if op.type == 3 and op.mem.base not in (RIP, 0) and op.mem.disp == 0 and op.mem.index == 0 \
                    and op.size == 8 and i.reg_name(op.mem.base) != "rsp":
                seen[i.address] = txt(i)
check("Z1 the displacement-0 qword accesses are exactly the classified six",
      set(seen) == set(EXPECT_SLOT0) | set(EXPECT_OTHER), str({"%08X" % a: s for a, s in seen.items()}))
for a, s in EXPECT_SLOT0.items():
    check("Z1 slot +0 %08X" % a, seen.get(a) == s, seen.get(a, "-"))
b450 = [txt(i) for i in body(0x0032E450) if "rax - 0x18]" in i.op_str or "rax + 0x38]" in i.op_str]
check("Z1 the biased init cursor never touches slot +0 or +0x50", not b450, str(b450))
pin("Z1 0032E725's base is a slot: pool + (id & 0x3F) << 7", 0x0032E6F5, "shl rcx, 7")
pin("Z1 ...pool", 0x0032E6EB, "lea rax, [rip + 0x1f94ace]")

# ---- Z2: the part callback slot
p50 = {}
for f in MOD:
    for i in body(f):
        for op in i.operands:
            if op.type == 3 and op.mem.base not in (RIP, 0) and op.mem.disp == 0x50 and i.reg_name(op.mem.base) != "rsp":
                p50[i.address] = txt(i)
check("Z2 +0x50 accesses", set(p50) == {0x0032E6FF, 0x0032E959, 0x0032E3B4}, str({"%08X" % a: s for a, s in p50.items()}))
pin("Z2 r14 = 0 in 0032E620", 0x0032E670, "xor r14d, r14d")
r14w = [i for i in body(0x0032E620) if 0x0032E670 < i.address < 0x0032E725 and i.op_str.startswith(("r14", "r14d"))]
check("Z2 r14 not rewritten before the stores", not r14w, str([("%08X" % i.address, txt(i)) for i in r14w]))
pin("Z2 0032E959 stores 0", 0x0032E959, "mov qword ptr [r10 + 0x50], 0")

# ---- Z3: indirect calls in the module
ind = []
for f in MOD:
    seq = body(f)
    for k, i in enumerate(seq):
        if i.mnemonic == "call" and not i.op_str.startswith("0x"):
            setup = [txt(x) for x in seq[max(0, k - 6):k] if x.op_str.startswith(("rcx,", "ecx,", "rdx,", "edx,"))]
            ind.append(("%08X" % i.address, txt(i), setup))
for a, s, st in ind:
    print("   indirect %s %s  args: %s" % (a, s, st))
slot_args = [a for a, s, st in ind if any(x in ("mov rcx, rbx", "mov rcx, rdi") for x in st)]
check("Z3 indirect calls found (control: the part callback at 0032E3C4 region)", any(a.startswith("0032E3") for a, _, _ in ind))
check("Z3 the five indirect calls: four pass +0x60 (and +0x70), one is the part callback", [a for a, _, _ in ind] ==
      ["0032E189", "0032E30C", "0032E34F", "0032E392", "0032E3C2"] and not slot_args, str(ind))
pin("Z3 0032E3C2 is reached with rcx = the slot: 0032E3B0 keeps it", 0x0032E3B4, "mov rax, qword ptr [rcx + 0x50]")

print("FAILS", FAILS)
sys.exit(1 if FAILS else 0)
