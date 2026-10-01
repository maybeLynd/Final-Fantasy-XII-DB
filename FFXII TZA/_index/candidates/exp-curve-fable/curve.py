"""curve.py - the experience curve 002F8F20, executed from the certified image (FABLE, Claude Opus 5.5, 2026-09-29).
NATIVE EXECUTION of the original bytes under unicorn (isolated function; no game process).

  X  EXECUTE: 002F8F20(n) for n = 0 .. 100, with the image's .text and .rdata mapped at their virtual addresses
  B  THE BODY: the linear coefficient starts at `lea edx, [rcx + 0x16]` AFTER `mov ecx, 2`, i.e. 0x18 = 24 at k = 2, and
     steps by 12 (`add edx, 0xc`): the term is trunc(0.4f * k^3 + 12 k^2)
  F  FORMULA: the executed values equal sum_{k=2}^{n+1} trunc(float32(k^3) * 0.4f + float32(12 k^2)) for n = 1 .. 98, 0 for
     n < 1 and -1 for n > 98 - and they DIFFER from the pages' k(12k - 2) = 12k^2 - 2k reading (level 2: 51, not 47)
  K  sensitivity: the pages' formula is computed the same way and is shown to disagree with the execution at every n >= 1
"""
import hashlib, os, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RAX, UC_X86_REG_RSP, UC_X86_REG_RIP
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
        for i in range(n)]
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
uc = Uc(UC_ARCH_X86, UC_MODE_64)
for nm, vs, va, rs, ro in SECS:
    if nm in (b".text", b".rdata"):
        base = (B + va) & ~0xFFF; size = ((B + va + max(vs, rs) + 0xFFF) & ~0xFFF) - base
        uc.mem_map(base, size); uc.mem_write(B + va, d[ro:ro + rs])
STACK = 0x10000000; uc.mem_map(STACK, 0x10000); RET = 0x20000000; uc.mem_map(RET, 0x1000); uc.mem_write(RET, b"\xC3")
def run(nv):
    uc.reg_write(UC_X86_REG_RSP, STACK + 0x8000); uc.mem_write(STACK + 0x8000, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RCX, nv & 0xFFFFFFFF)
    uc.emu_start(0x2F8F20, RET, count=100000)
    return struct.unpack("<i", struct.pack("<I", uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF))[0]
got = {k: run(k) for k in range(0, 101)}
check("X", got[0] == 0 and got[99] == -1 and got[100] == -1 and all(got[k] > 0 for k in range(1, 99)),
      "executed: n=0 -> %d, n=1 -> %d, n=2 -> %d, n=98 -> %d, n=99 -> %d" % (got[0], got[1], got[2], got[98], got[99]))
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def f32(x): return struct.unpack("<f", struct.pack("<f", x))[0]   # round to IEEE single, as cvtdq2ps/mulss/addss do
off = lambda v: next(v - B - va + ro for nm, vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
body = {x.address: ("%s %s" % (x.mnemonic, x.op_str)) for x in cs.disasm(d[off(0x2F8F20):off(0x2F8F9A)], 0x2F8F20)}
check("B", body.get(0x2F8F3E) == "mov ecx, 2" and body.get(0x2F8F46) == "lea edx, [rcx + 0x16]" and body.get(0x2F8F87) == "add edx, 0xc"
      and struct.unpack_from("<f", d, off(0x9153EC))[0] == f32(0.4),
      "ecx = 2 before the lea, so the coefficient starts at 0x18 = 24 and steps by 12; the cubic factor is 0.4f")
def curve(nv, lin):
    if nv < 1: return 0
    if nv > 98: return -1
    return int(sum(int(f32(f32(f32(k ** 3) * f32(0.4)) + f32(lin(k)))) for k in range(2, nv + 2)))   # cvttss2si truncates
mine = {k: curve(k, lambda k: 12 * k * k) for k in range(101)}
pages = {k: curve(k, lambda k: k * (12 * k - 2)) for k in range(101)}
check("F", all(mine[k] == got[k] for k in range(101)),
      "executed == sum trunc(0.4f k^3 + 12k^2) for every n 0..100; thresholds: level 2 = %d, level 10 = %d, level 50 = %d, level 99 = %d"
      % (got[1], got[9], got[49], got[98]))
diff = [k for k in range(1, 99) if pages[k] != got[k]]
check("K", len(diff) == 98, "the pages' k(12k-2) reading differs from the execution at %d of 98 levels (level 2: pages %d, executed %d)"
      % (len(diff), pages[1], got[1]))
with open(os.path.join(HERE, "curve.tsv"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("n (level - 1)\texp to reach level n+1 (executed)\n" + "\n".join("%d\t%d" % (k, got[k]) for k in range(101)) + "\n")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
