"""ctor_claims.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.
Audit of the store's rows that say a constructor does NOT write their bytes, after motion_blur_ctor.py found one such claim
false (a reading that stopped before the constructor's loop). Each constructor is read whole, with the callees it hands
`this` (or this + k) to and its memset calls.

  A  EIGHT CLAIMS HOLD. The named constructor chain writes none of the row's bytes:
       PShadowCaster +0x54 (006C0EB0: +0x00..+0x1F, +0x50, then the sampler at +0x58), PConstantBufferD3D11 +0x0C / +0x4C
       (00611D60: 005DBF20 writes +0x00 / +0x08; then +0x10..+0x2F, +0x30..+0x47, +0x48), PStructuredBufferD3D11 +0x14 / +0x64
       (006127C0: 005DCBD0 writes +0x00..+0x10; then +0x18, +0x48..+0x63), OrderedCommandList +0x2B (0018AD00: +0x00..+0x17,
       +0x20, +0x24, word +0x29, +0x2C), RenderContext02CC0410 +0x16C (00615840: +0x108..+0x11F, memsets +0x170 / +0x2F8 for
       0x188 each), GameSettingConfig +0x448 (001DE050: memset +0x7C for 0x3CC, ending exactly at +0x448; +0x44C, +0x658..)
  C  control: the same coverage sees the neighbours - RenderContext +0x108 / +0x170 (memset), GameSettingConfig +0x447
     (memset end) / +0x44C, OrderedCommandList +0x29 / +0x2C, PShadowCaster +0x50 / +0x58 (through 00615CD0) - so A's
     empty results are not a blind instrument
  Z  TWO NEED A QUALIFIER. ManagerSub8FA0SlotRecord02B8 +0xC8 ('the initialiser writes nothing here') and +0x296 ('untouched
     by the constructor'): the record is built by 002C0F30 through the in-place widget constructor 00245000 (edx = 0x2B8), and
     00245000 -> 002465F0 memsets the whole object first (00861EC0 at 00246626, size = edx sign-extended at 00246612). So the
     bytes ARE written - to zero - at construction; the claims hold only for 002C0F30's own stores
  W  REGRESSION (FAILS before): both rows carry the zero-initialisation qualifier
Usage: python ctor_claims.py [--patch]
"""
import hashlib, os, re, struct, sys, bisect
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}
MEM = re.compile(r"(byte|word|dword|qword|xmmword) ptr \[(\w+)(?: \+ (0x[0-9a-f]+))?\]")
def body(a, n):
    out = []
    for x in cs.disasm(d[off(a):off(a) + n], a):
        out.append(x)
        if x.mnemonic == "ret": break
    return out
def coverage(fn, n, this_off=0, depth=0):
    """Bytes of the object written by fn(rcx = object + this_off): its own stores through registers holding this + k,
    the callees it passes this + k in rcx, and memset (00861EC0) with rcx = this + k, r8 = an immediate size."""
    regs = {"rcx": this_off}; cov = set(); last = {}
    for x in body(fn, n):
        ops = [s.strip() for s in x.op_str.split(",")]
        if x.mnemonic == "mov" and len(ops) == 2 and ops[1] in regs and not MEM.search(ops[0]): regs[ops[0]] = regs[ops[1]]
        elif x.mnemonic == "lea" and len(ops) == 2:
            m = re.fullmatch(r"\[(\w+) \+ (0x[0-9a-f]+)\]", ops[1])
            if m and m.group(1) in regs: regs[ops[0]] = regs[m.group(1)] + int(m.group(2), 16)
            elif ops[0] in regs: del regs[ops[0]]
        elif x.mnemonic == "add" and len(ops) == 2 and ops[0] in regs and ops[1].startswith("0x"): regs[ops[0]] += int(ops[1], 16)
        elif x.mnemonic in ("mov", "and", "or", "xor", "add", "sub", "movups", "movaps", "movdqu") and ops:
            m = MEM.search(ops[0])
            if m and m.group(2) in regs:
                o = regs[m.group(2)] + (int(m.group(3), 16) if m.group(3) else 0); cov.update(range(o, o + W[m.group(1)]))
            elif ops[0] in regs and x.mnemonic == "mov": del regs[ops[0]]
        if x.mnemonic == "mov" and len(ops) == 2 and ops[0] in ("r8d", "r8") and ops[1].startswith("0x"): last["r8"] = int(ops[1], 16)
        if x.mnemonic == "call":
            if x.op_str == "0x861ec0" and "rcx" in regs and "r8" in last: cov.update(range(regs["rcx"], regs["rcx"] + last["r8"]))
            elif x.op_str.startswith("0x") and "rcx" in regs and depth < 2: cov |= coverage(int(x.op_str, 16), 0x400, regs["rcx"], depth + 1)
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"): regs.pop(r, None)
            last.pop("r8", None)
    return cov
CLAIMS = [("PShadowCaster", 0x6C0EB0, 0xA1, 0x54, 4), ("PConstantBufferD3D11", 0x611D60, 0x64, 0x0C, 4), ("PConstantBufferD3D11", 0x611D60, 0x64, 0x4C, 4),
          ("PStructuredBufferD3D11", 0x6127C0, 0x5A, 0x14, 4), ("PStructuredBufferD3D11", 0x6127C0, 0x5A, 0x64, 4), ("OrderedCommandList", 0x18AD00, 0x69, 0x2B, 1),
          ("RenderContext02CC0410", 0x615840, 0x377, 0x16C, 4), ("GameSettingConfig", 0x1DE050, 0x125, 0x448, 4)]
res = []
for t, fn, n, o, w in CLAIMS:
    this0 = 0
    if t in ("PConstantBufferD3D11", "PStructuredBufferD3D11"): fn_rcx = None   # placement constructors: the object arrives in rdx
    cov = coverage(fn, n) if t not in ("PConstantBufferD3D11", "PStructuredBufferD3D11") else None
    if cov is None:   # rdx holds the object: re-run with rdx seeded
        src = body(fn, n); regs_seed = {"rdx": 0}
        cov = set()
        for x in src:
            ops = [s.strip() for s in x.op_str.split(",")]
            if x.mnemonic == "mov" and len(ops) == 2 and ops[1] == "rdx" and not MEM.search(ops[0]): regs_seed[ops[0]] = 0
            m = MEM.search(ops[0]) if ops else None
            if m and m.group(2) in regs_seed and x.mnemonic.startswith("mov"):
                o2 = regs_seed[m.group(2)] + (int(m.group(3), 16) if m.group(3) else 0); cov.update(range(o2, o2 + W[m.group(1)]))
            if x.mnemonic == "lea" and len(ops) == 2:
                mm = re.fullmatch(r"\[(\w+) \+ (0x[0-9a-f]+)\]", ops[1])
                if mm and mm.group(1) in regs_seed: regs_seed[ops[0]] = int(mm.group(2), 16)
            if x.mnemonic == "call" and x.op_str.startswith("0x") and x.op_str != "0x861ec0":
                cov |= coverage(int(x.op_str, 16), 0x80, 0, 1)   # the base constructor is called with rcx = the object
    res.append((t, o, [b for b in range(o, o + w) if b in cov]))
check("A", all(not hit for t, o, hit in res), "no constructor-chain store covers the claimed bytes: %s" % [(t, hex(o), hit) for t, o, hit in res])
ctl = [0x108 in coverage(0x615840, 0x377), 0x170 in coverage(0x615840, 0x377), 0x447 in coverage(0x1DE050, 0x125), 0x44C in coverage(0x1DE050, 0x125),
       0x29 in coverage(0x18AD00, 0x69), 0x2C in coverage(0x18AD00, 0x69), 0x50 in coverage(0x6C0EB0, 0xA1), 0x58 in coverage(0x6C0EB0, 0xA1)]
check("C", ctl == [True] * 8, "the coverage sees the neighbouring stores and memsets: %s" % ctl)
A2 = {x.address: (x.mnemonic, x.op_str) for x in body(0x2465F0, 0x60)}
Z0 = {x.address: (x.mnemonic, x.op_str) for x in body(0x245000, 0x20)}
check("Z", Z0.get(0x245011) == ("call", "0x2465f0") and A2.get(0x246612) == ("movsxd", "r8, edx") and A2.get(0x246618) == ("xor", "edx, edx")
      and A2.get(0x24661D) == ("mov", "rdi, rcx") and A2.get(0x246626) == ("call", "0x861ec0")
      and any(x.mnemonic == "mov" and x.op_str == "edx, 0x2b8" for x in cs.disasm(d[off(0x2C0F70):off(0x2C0F90)], 0x2C0F70)),
      "00245000 -> 002465F0 memsets the object for edx bytes (00861EC0 at 00246626); 002C0F30 passes edx = 0x2B8")
REC = "_index/candidates/ctor-claims-audit-opus/ctor_claims.py"
NOTE = (" || ZERO-INITIALISED, qualifier 2026-09-28 (OPUS, %s Z): the record is built through the in-place widget constructor 00245000 "
        "(edx = 0x2B8), whose 002465F0 memsets all 0x2B8 bytes first (00861EC0 at 00246626). 'Writes nothing' / 'untouched' holds for "
        "002C0F30's own stores only: these bytes are zero after construction." % REC)
FI = os.path.join(DB, "_types", "fields.tsv")
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "ManagerSub8FA0SlotRecord02B8" and c[1] in ("0x0C8", "0x296") and REC not in c[5]:
            c[5] += NOTE; fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
rows = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "ManagerSub8FA0SlotRecord02B8" and cells(l)[1] in ("0x0C8", "0x296")]
check("W", len(rows) == 2 and all(NOTE in r[5] for r in rows), "both ManagerSub8FA0SlotRecord02B8 rows carry the zero-initialisation qualifier")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
