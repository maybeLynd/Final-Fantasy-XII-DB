"""falsify_apply_result.py - falsification pass 1 on 07-Combat-Action/CONTRACT-apply-result-to-target.md
(OPUS, 2026-09-30). Static; reads only the shipping image. Each check is one of the contract's clauses at its bytes.

A1  §2 003112F0 is 2,040 bytes; 00311321 and 0031132C call the owner resolver 0031B860
A2  §2 the numeric dispatch: bit 8 at 00311610, bit 14 at 0031166D, byte +0x1D at 003116A6 -> 00300BC0, the source test at
    003116FB, bit 7 at 00311703 (test dl, dl / jns), bit 13 at 00311748 (bt r9d, 0xd), and the source-MP flags built at
    00311753-0031176A as (~(f >> 7) & 0x10) | ((f >> 10) & 0x20)
A3  I1 the apply and remove loops call 0030E360 with mode 3 and mode 0, flags ((+0x140 & 0x10) | 0x1000) >> 3 and
    ((+0x140 & 0x20) | 0x2000) >> 4
A4  I2 003115B6-00311606 copies non-negative dwords to target +0xBC + 4i and non-negative words to target +0x13C + 2i
A5  I3 r14d = 1 at 0031153F, 003115A4, 003117D0, 0031180C with no result test; 00311AAF-00311AC5 calls 0030FED0(target, 0)
    only for a target, callerFlags without 0x200, and the dirty flag
A6  §3 the layer loops at 00311788 (two bytes from +0x3C) and 003117E4 (four bytes from +0x3E) call 0030E130
A7  I6 the target HP pair 00300520 / 00300530 and the MP pair 00300C90 / 00300CE0 are both called
A8  I8 the gate 00385BA0 ANDs spawn +0x14 with 0xFB, 0xFD, 0xFE at 00385C17, 00385C41, 00385C6B; the applier calls it at
    0031137A; the steal loop's btr is at 0031146C
A9  I7 there is no unconditional 0x400 in the target-HP flag build (00311610-0031166D)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext = R.at, R.md, R.ext
F = 0x003112F0
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


b = list(md.disasm(at(F, ext[F]), F))


def win(lo, hi):
    return ["%s %s" % (i.mnemonic, i.op_str) for i in b if lo <= i.address <= hi]


def ins(a):
    i = R.dec(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def calls_to(t, lo=F, hi=None):
    hi = hi or F + ext[F]
    return [i.address for i in b if lo <= i.address < hi and i.mnemonic == "call" and i.operands[0].type == X.X86_OP_IMM and i.operands[0].imm == t]


check("A1", ext[F] == 2040 and ins(0x00311321) == "call 0x31b860" and ins(0x0031132C) == "call 0x31b860",
      "extent %d B; %s; %s" % (ext[F], ins(0x00311321), ins(0x0031132C)))

g = {"bit 8 @00311610": ins(0x00311610), "bit 14 @0031166D": ins(0x0031166D), "+0x1D @003116A6": ins(0x003116A6),
     "source @003116FB": ins(0x003116FB), "bit 7 @00311703": ins(0x00311703), "bit 13 @00311748": ins(0x00311748)}
f13 = win(0x00311753, 0x0031176A)
ok2 = ("0x100" in g["bit 8 @00311610"] or ", 8" in g["bit 8 @00311610"]) and ("0x4000" in g["bit 14 @0031166D"] or "0xe" in g["bit 14 @0031166D"]) \
    and "0x1d]" in g["+0x1D @003116A6"] and g["bit 7 @00311703"] == "test dl, dl" and g["bit 13 @00311748"] == "bt r9d, 0xd" \
    and any(x.startswith("shr") and x.endswith(", 7") for x in f13) and any(x.startswith("not") for x in f13) \
    and any(x.endswith(", 0x10") and x.startswith("and") for x in f13) and any(x.endswith(", 0xa") and x.startswith("shr") for x in f13) \
    and any(x.endswith(", 0x20") and x.startswith("and") for x in f13) and calls_to(0x00300BC0)
check("A2", ok2, "%s; source-MP flag build %s; 00300BC0 called at %s" % (g, f13, ["%08X" % a for a in calls_to(0x00300BC0)]))

e360 = calls_to(0x0030E360)
# the mode is the 7th argument ([rsp + 0x30]): an immediate 3 in the apply loop, r13d in the remove loop, where
# 00311560 zeroes r13d and nothing writes it before the call
modes = []
for a in e360:
    k = next(j for j, i in enumerate(b) if i.address == a)
    w = next(w for w in reversed(b[max(0, k - 30):k]) if w.op_str.startswith("dword ptr [rsp + 0x30], "))
    src = w.op_str.split(", ")[1]
    if src.startswith("0x") or src.isdigit():
        m = int(src, 0)
    else:
        zero = [i for i in b if i.address < w.address and i.mnemonic == "xor" and i.op_str == "%s, %s" % (src, src)]
        later = [i for i in b if zero and zero[-1].address < i.address < w.address and i.op_str.split(",")[0] in (src, src.replace("d", ""))]
        m = 0 if zero and not later else src
    modes.append((a, m))
# the flags: (+0x140 & 0x10) with bit 12 set (bts eax, 0xc = | 0x1000) then >> 3; (& 0x20) with bit 13 set then >> 4
fl = win(0x003114D2, 0x003114EE)
ok3 = [m for _, m in modes] == [3, 0] and fl == ["mov ecx, dword ptr [rbx + 0x140]", "mov eax, ecx", "and eax, 0x10", "and ecx, 0x20",
                                               "bts eax, 0xc", "bts ecx, 0xd", "shr ecx, 4", "shr eax, 3", "mov dword ptr [rsp + 0x40], ecx"]
check("A3", ok3, "0030E360 calls with mode %s; flag build %s" % (["%08X:%s" % (a, m) for a, m in modes], fl))

# I2: r9 = target - record, a cursor from record + 0x5C, the store at [r9 + rcx + 0x60] = target + 0xBC + 4i; 32 entries;
# negatives skipped. The word copy repeats the scheme from record + 0xDC to target + 0x13C
cp = win(0x003115B6, 0x00311606)
ok4 = "sub r9, rbx" in cp and "lea rcx, [rbx + 0x5c]" in cp and "mov r8d, 0x20" in cp and "js 0x3115db" in cp     and "mov dword ptr [r9 + rcx + 0x60], eax" in cp and "lea rax, [rbx + 0xdc]" in cp     and "mov word ptr [rax + r9 + 0x60], cx" in cp and "js 0x3115fe" in cp and 0x5C + 0x60 == 0xBC and 0xDC + 0x60 == 0x13C
check("A4", ok4, "dword copy: r9 = target - record, cursor record + 0x5C, store [r9 + rcx + 0x60] (= target + 0xBC), 0x20 entries, "
      "negatives skipped; word copy from record + 0xDC to target + 0x13C: %s" % ok4)

# I3: the dirty sets, and the outer tail's three tests: target, the local [rsp + 0x44] = (callerFlags >> 9) & 1, and r14d
dirty = [ins(a) for a in (0x0031153F, 0x003115A4, 0x003117D0, 0x0031180C)]
bit9 = win(0x00311344, 0x00311350)
tail = win(0x00311AAF, 0x00311AC5)
ok5 = all(x == "mov r14d, 1" for x in dirty) and bit9 == ["mov eax, r10d", "mov r14d, r13d", "shr eax, 9", "and eax, 1", "mov dword ptr [rsp + 0x44], eax"]     and "cmp dword ptr [rsp + 0x44], 0" in tail and "test r14d, r14d" in tail and "test rdi, rdi" in tail     and calls_to(0x0030FED0, 0x00311AAF, 0x00311AD0) and "xor edx, edx" in win(0x00311AAF, 0x00311AD0)
check("A5", ok5, "dirty sets %s; [rsp + 0x44] = %s; outer tail %s" % (dirty, bit9, tail))

l1, l2 = win(0x00311788, 0x003117E3), win(0x003117E4, 0x00311830)
ok6 = calls_to(0x0030E130, 0x00311788, 0x003117E4) and calls_to(0x0030E130, 0x003117E4, 0x00311840) \
    and any("0x3c]" in x or "0x3c" in x for x in win(0x00311770, 0x003117A0)) and any("0x3e" in x for x in win(0x003117D0, 0x00311800))
check("A6", bool(ok6), "0030E130 calls in the two loops %s / %s" % (
    ["%08X" % a for a in calls_to(0x0030E130, 0x00311788, 0x003117E4)], ["%08X" % a for a in calls_to(0x0030E130, 0x003117E4, 0x00311840)]))

direct = {"%08X" % t: ["%08X" % a for a in calls_to(t)] for t in (0x00300520, 0x00300530, 0x00300C90, 0x00300CE0)}
# the setters may be chosen by a cmov on a function address and called indirectly: accept a lea of the address too
leas = set()
for i in b:
    if i.mnemonic == "lea" and i.operands[1].type == X.X86_OP_MEM and i.operands[1].mem.base == X.X86_REG_RIP:
        leas.add(i.address + i.size + i.operands[1].mem.disp)
ok7 = all(direct["%08X" % t] or t in leas for t in (0x00300520, 0x00300530, 0x00300C90, 0x00300CE0))
check("A7", ok7, "direct calls %s; addresses loaded by lea %s" % (direct, ["%08X" % t for t in (0x00300520, 0x00300530, 0x00300C90, 0x00300CE0) if t in leas]))

gb = list(md.disasm(at(0x00385BA0, ext[0x00385BA0]), 0x00385BA0))
ands = {a: next(("%s %s" % (i.mnemonic, i.op_str) for i in gb if i.address == a), None) for a in (0x00385C17, 0x00385C41, 0x00385C6B)}
ok8 = all(x and x.startswith("and") and "+ 0x14]" in x for x in ands.values()) and \
    sorted(x.split(", ")[1] for x in ands.values()) == ["0xfb", "0xfd", "0xfe"] and ins(0x0031137A) == "call 0x385ba0" and ins(0x0031146C).startswith("btr")
check("A8", ok8, "gate %s; 0031137A `%s`; 0031146C `%s`" % (ands, ins(0x0031137A), ins(0x0031146C)))

hp = win(0x00311610, 0x0031166D)
check("A9", not any("0x400" in x.split(", ")[-1] and x.startswith(("or", "mov")) for x in hp),
      "immediate 0x400 in the target-HP flag build: %s" % [x for x in hp if "0x400" in x])

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
