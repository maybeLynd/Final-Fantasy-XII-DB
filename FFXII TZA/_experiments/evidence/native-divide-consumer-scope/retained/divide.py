"""divide.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
ScriptVM OPDIV (0x15, 0025F0AC) and OPMOD (0x16, 0025F1D6), for ASTRA-REQ-OPUS-SCRIPT-DIVISION-GUARD (ASTRA 79) and
ASTRA-REQ-OPUS-SCRIPT-DIVIDE-OVERFLOW (ASTRA 80). Written from the bytes; ASTRA's records are the executed evidence.

  I  OPDIV INTEGER PATH: 00267560 gates it; the first pop (00267E10) is the divisor (ebx), the second the dividend (eax);
     the only test before the divide is `test ebx, ebx / je 0025E682`, whose target pushes int 0 (tag ebp = 1, payload 0);
     then `cdq / idiv ebx / mov ecx, eax / jmp 0025E68C`. No compare of eax or ebx against -1 or 0x80000000 sits between
  F  OPDIV FLOAT PATH: the top pops to xmm6 (the divisor), the next to xmm0 (the dividend); a tag of 1 converts with
     cvtdq2ps, 2 loads the float, any other tag (or an empty stack, after 008620C0) gives xmm7; `ucomiss xmm6, xmm7` then
     `jp` and `jne` both reach `divss xmm0, xmm6` (0025F1A3) and only ordered-equal takes `movaps xmm0, xmm7` - so a NaN
     divisor divides and a +0.0 or -0.0 divisor gives xmm7; the result is pushed with tag 2 while the depth is below 0x3F
  Z  THE BASELINE: the interpreter (0025E4C0, body 0025E550..00261DDB) sets ebp = 1 at 0025E555 and zeroes xmm7 at 0025E55F,
     and writes xmm7 nowhere else but its epilogue restore (00261DBC); xmm7 is nonvolatile under the Win64 ABI, so it is 0.0
     throughout the body for conforming callees
  M  OPMOD: two pops, then `cdq / idiv ebx` with NO test of ebx at all; the remainder edx is pushed as an int
  U  NO CATCHING FRAME TO THE FRAME TICK: the RUNTIME_FUNCTION covering 0025F0DA (0025E550, chained to 0025E4C0) has no
     handler; its only direct caller 0025E0D3 is in 0025DF00, whose personality is __GSHandlerCheck (00808BA8, cookie check
     only); the direct-caller chain 0025D9E0 -> 00314020 -> {0022A770, 0022B8C0, 0022BC20} -> 0022A580 -> 0022A490 ->
     0017D6E0 -> 0017CCD0 (GameApplication slot 4, the frame tick, reached only through the vtable) installs no handler
  C  CONTROLS: the U walk's handler reader does report 00808BA8 on 0025DF00, so it detects a personality when one is there;
     a parity-dropped model (jp removed: NaN substitutes) and a reversed division (divss xmm6, xmm0) are rejected by F;
     an OPDIV model with a quotient guard is rejected by I
So INT_MIN / -1 reaches `idiv` in OPDIV's integer path and in OPMOD, and INT_MIN % -1 and x % 0 reach it in OPMOD. IDIV
raises #DE for a quotient that does not fit (Intel SDM, IDIV); ASTRA 80 observed exactly that stop in an isolated guest.
Not claimed: what the process does with #DE above the frame tick (the main loop, the CRT frame, the unhandled-exception
filter: ASTRA's native-exception-filter-tail), whether any authored script supplies these operands, flags or MXCSR.
Usage: python divide.py
"""
import bisect, hashlib, os, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_REG_XMM7, X86_REG_EBP, X86_REG_RBP
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP, fast_load=True); pe.parse_data_directories(directories=[3])
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def dis(lo, hi): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)]
def seq(lo, hi): return [(m, o) for a, m, o in dis(lo, hi)]
# I
I = dis(0x25F0AC, 0x25F0E3)
check("I", seq(0x25F0AC, 0x25F0E3) == [("mov", "rcx, r10"), ("call", "0x267560"), ("test", "eax, eax"), ("je", "0x25f0e3"), ("lea", "r12, [rip + 0x1e3aa01]"),
                                      ("mov", "rcx, r12"), ("call", "0x267e10"), ("mov", "rcx, r12"), ("mov", "ebx, eax"), ("call", "0x267e10"),
                                      ("test", "ebx, ebx"), ("je", "0x25e682"), ("cdq", ""), ("idiv", "ebx"), ("mov", "ecx, eax"), ("jmp", "0x25e68c")]
      and seq(0x25E682, 0x25E68A) == [("xor", "r11d, r11d"), ("mov", "ecx, r11d"), ("jmp", "0x25e68f")]
      and ("mov", "byte ptr [r9 + r10 + 4], bpl") in seq(0x25E68F, 0x25E6C2) and ("mov", "dword ptr [r10 + r9*4 + 0x184], ecx") in seq(0x25E68F, 0x25E6C2),
      "OPDIV int: divisor = first pop (ebx), dividend = second; only `test ebx, ebx / je 0025E682` (push int 0) precedes cdq / idiv ebx")
# F
F = seq(0x25F0E3, 0x25F1D6)
Fd = {a: (m, o) for a, m, o in dis(0x25F0E3, 0x25F1D6)}
check("F", Fd.get(0x25F111) == ("movss", "xmm6, dword ptr [r10 + rdx*4 + 0x184]") and Fd.get(0x25F127) == ("cvtdq2ps", "xmm6, xmm6") and Fd.get(0x25F141) == ("movaps", "xmm6, xmm7")
      and Fd.get(0x25F164) == ("movss", "xmm0, dword ptr [r10 + rdx*4 + 0x184]") and Fd.get(0x25F17A) == ("cvtdq2ps", "xmm0, xmm0") and Fd.get(0x25F194) == ("movaps", "xmm0, xmm7")
      and Fd.get(0x25F197) == ("ucomiss", "xmm6, xmm7") and Fd.get(0x25F19A) == ("jp", "0x25f1a3") and Fd.get(0x25F19C) == ("jne", "0x25f1a3")
      and Fd.get(0x25F19E) == ("movaps", "xmm0, xmm7") and Fd.get(0x25F1A3) == ("divss", "xmm0, xmm6")
      and Fd.get(0x25F1AA) == ("cmp", "r9d, 0x3f") and Fd.get(0x25F1B3) == ("mov", "byte ptr [rax + r10 + 4], 2") and Fd.get(0x25F1C7) == ("movss", "dword ptr [r10 + rax*4 + 0x184], xmm0")
      and Fd.get(0x25F109) == ("sub", "ecx, ebp") and Fd.get(0x25F10B) == ("je", "0x25f11d") and Fd.get(0x25F10F) == ("jne", "0x25f141"),
      "OPDIV float: top -> xmm6 divisor, next -> xmm0 dividend; ucomiss xmm6, xmm7 / jp / jne -> divss xmm0, xmm6; only ordered-equal substitutes xmm7; tag 2 result")
# Z
cs.detail = True
wx, we = [], []
for lo, hi in ((0x25E4C0, 0x25E550), (0x25E550, 0x261DDB)):
    for x in cs.disasm(d[off(lo):off(hi)], lo):
        try: _, wr = x.regs_access()
        except Exception: continue
        if X86_REG_XMM7 in wr: wx.append(x.address)
        if X86_REG_EBP in wr or X86_REG_RBP in wr: we.append((x.address, x.mnemonic))
cs.detail = False
Zd = {a: (m, o) for a, m, o in dis(0x25E550, 0x25E567)}
check("Z", wx == [0x25E55F, 0x261DBC] and Zd.get(0x25E555) == ("mov", "ebp, 1") and Zd.get(0x25E55F) == ("xorps", "xmm7, xmm7")
      and [a for a, m in we if a >= 0x25E550 and m not in ("pop", "push")] == [0x25E555],
      "the interpreter writes xmm7 only at 0025E55F (zero) and 00261DBC (restore); ebp only at 0025E555 (= 1) besides push/pop; ebp writes %s" % [hex(a) for a, m in we])
# M
check("M", seq(0x25F1D6, 0x25F226) == [("mov", "rcx, r10"), ("call", "0x267e10"), ("lea", "rcx, [rip + 0x1e3a8db]"), ("mov", "ebx, eax"), ("call", "0x267e10"),
                                      ("movsxd", "r9, dword ptr [rip + 0x1e3a8cd]"), ("cdq", ""), ("idiv", "ebx"), ("xor", "r11d, r11d"), ("cmp", "r9d, 0x3f"),
                                      ("jge", "0x25f226"), ("lea", "r10, [rip + 0x1e3a8ba]"), ("mov", "byte ptr [r9 + r10 + 4], bpl"), ("mov", "byte ptr [r9 + r10 + 0x44], 6"),
                                      ("mov", "dword ptr [r10 + r9*4 + 0x84], r11d"), ("mov", "dword ptr [r10 + r9*4 + 0x184], edx"), ("jmp", "0x25e6c2")],
      "OPMOD: two pops, cdq / idiv ebx with no test of the divisor; the remainder edx is pushed as an int")
# U
exc = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]; eo = pe.get_offset_from_rva(exc.VirtualAddress)
RF = [struct.unpack_from("<III", d, eo + 12 * i) for i in range(exc.Size // 12)]; ST = [r[0] for r in RF]
def rf(va):
    i = bisect.bisect_right(ST, va - B) - 1
    return RF[i] if i >= 0 and RF[i][0] <= va - B < RF[i][1] else None
def personality(u):
    uo = pe.get_offset_from_rva(u & ~1); fl = d[uo] >> 3; after = uo + 4 + 2 * ((d[uo + 2] + 1) & ~1)
    h, prim = (struct.unpack_from("<I", d, after)[0] + B if fl & 3 else None), None
    if fl & 4:
        cb, ce, cu = struct.unpack_from("<III", d, after); h2, p2 = personality(cu); h = h or h2; prim = p2 or cb + B
    return h, prim
text = [s for s in pe.sections if s.Name.startswith(b".text")][0]; ts, tb = text.VirtualAddress, text.get_data()
callers = {}
for i in range(len(tb) - 5):
    if tb[i] in (0xE8, 0xE9):
        callers.setdefault(B + ts + i + 5 + struct.unpack_from("<i", tb, i + 1)[0], []).append(B + ts + i)
chain, frames, f = [], {}, 0x25E4C0
h0, p0 = personality(rf(0x25F0DA)[2])
level = [0x25E4C0]
while level:
    nxt = []
    for fn in level:
        for s in callers.get(fn, []):
            h, prim = personality(rf(s)[2]); e = prim or rf(s)[0] + B
            if e not in frames: frames[e] = h; nxt.append(e)
    level = nxt
want = {0x25DF00: 0x808BA8, 0x25D9E0: None, 0x314020: None, 0x22A770: None, 0x22B8C0: None, 0x22BC20: None, 0x22A580: None, 0x22A490: None, 0x17D6E0: None, 0x17CCD0: None}
check("U", h0 is None and p0 == 0x25E4C0 and rf(0x25F0DA)[0] + B == 0x25E550 and callers.get(0x25E4C0) == [0x25E0D3] and frames == want and not callers.get(0x17CCD0),
      "0025F0DA's frame (0025E550 chained to 0025E4C0) has no handler; direct callers up to 0017CCD0: %s" % {hex(k): (hex(v) if v else None) for k, v in frames.items()})
# C
check("C", frames.get(0x25DF00) == 0x808BA8 and ("jp", "0x25f1a3") in F and ("divss", "xmm6, xmm0") not in F
      and not any(m == "cmp" and ("0x80000000" in o or "-1" in o or "0xffffffff" in o) for m, o in seq(0x25F0AC, 0x25F0E3)),
      "controls: the handler reader reports 00808BA8 on 0025DF00; F keeps jp and rejects reversed division; I holds no quotient guard")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
