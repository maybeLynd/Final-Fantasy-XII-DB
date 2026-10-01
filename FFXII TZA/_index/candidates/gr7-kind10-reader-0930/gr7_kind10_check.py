"""gr7_kind10_check.py - GR-7: who reads operand-store kind 10, the per-unit mask 00312170 composes from action row
+0x3A / +0x13 / +0x0C bits 13-14? (OPUS, 2026-09-30). Static reads of the certified image plus a shipped-data census.

K1  the store: kind 10 is the battle unit's dword +0xB90 (index 0 only) - writer arm 00329F1C..00329F29 of the operand
    store writer 00329E60, reader arm 0032126F..0032127C of AiTargetSelector_ResolveOperandValue 00321190 (both jump
    tables decoded, case 10).
K2  00312170 composes the mask (bts from +0x3A in 1..0xFE, or from +0x13, bits 8/9 from +0x0C bits 13/14), ORs in the
    current value (00321190(10) at 00312248) and publishes it with 00329E60(10, unit, 0, mask) at 0031225E.
K3  every direct caller of 00321190 / 00329E60 with its kind: constant 10 at 00303088 (the selector), 00312248 /
    0031225E (the composer) and 002FE6E7 / 002FE74E (the AI store op, forced to 10 for order ids 0x4122 / 0x4123); the
    other callers pass constant 3 or a kind decoded from authored data (operand >> 12).
K4  the reader: AiOrder_EvaluateTargetSelector 00301AD0 takes a selector entry {u16 operand, u8 mode (+8), u8 opcode
    (+9), s16 param (+0xA)}; opcode 0x36 / 0x37 with mode 3 falls to the candidate loop, whose jump table sends cases
    54 / 55 to 00303079: read kind 10 of the candidate unit (r15) and `bt eax, esi` with esi = the param. Opcode 0x36
    requires the bit set, 0x37 clear (r12 = ~opcode & 1, compared at 00303069 through 003021D9).
K5  the AI store op 002FE660: order ids 0x4122 / 0x4123 force kind 10 on the unit 0031B7E0 resolves from +0x710, then
    bts (0x4122) / btr (0x4123) the order's param bit and write it back.
K6  the shipped data: the 256 player gambit target-condition rows (battle_pack directory +0x20) carry no opcode 0x36 /
    0x37, so no player gambit reads kind 10; the 166 .ard enemy order-set files (1,422 sets / 50,050 records) carry
    6,140 mode-3 0x36/0x37 entries testing bits 0-16 and 25-28, 31, and no authored dynamic kind (selector modes 0-2,
    store ops 0x4149 / 0x4155-0x4157) is ever 10 - kind 10 is reached only through the fixed paths above.
Prints PASS/FAIL per check and FAILS n last.
"""
import collections, glob, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
WORK = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work"))
sys.path.insert(0, KIT)
import retool as T  # noqa: E402
import regval as V  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
B = 0x120000
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


u32i = lambda a: struct.unpack("<I", R.at(a, 4))[0]
u8i = lambda a: R.at(a, 1)[0]

# K1
wtab = [B + u32i(B + 0x209F40 + 4 * k) for k in range(10)]
rtab = [B + u32i(B + 0x2012AC + 4 * k) for k in range(10)]
check("K1", txt(0x00329E64) == "dec ecx" and txt(0x003211A7) == "lea rcx, [rip - 0x2011ae]"
      and txt(0x00329E72) == "lea rcx, [rip - 0x209e79]" and wtab[9] == 0x00329F1C and rtab[9] == 0x0032126F
      and txt(0x00329F21) == "test r8d, r8d" and txt(0x00329F29) == "mov dword ptr [rdx + rax*4 + 0xb90], r9d"
      and txt(0x00321274) == "test r8d, r8d" and txt(0x0032127C) == "mov ecx, dword ptr [rdx + rax*4 + 0xb90]",
      "kind 10 = battle unit dword +0xB90, index 0: writer arm %08X, reader arm %08X" % (wtab[9], rtab[9]))
# K2
check("K2", txt(0x003121F5) == "movzx ecx, byte ptr [rdi + 0x3a]" and txt(0x00312203) == "bts ebx, eax"
      and txt(0x00312206) == "movzx eax, byte ptr [rdi + 0x13]" and txt(0x0031221E) == "and eax, 0x2000"
      and txt(0x0031222C) == "and edx, 0x4000" and txt(0x00312244) == "lea ecx, [r8 + 0xa]" and txt(0x00312248) == "call 0x321190"
      and txt(0x0031224D) == "or ebx, dword ptr [rsp + 0x30]" and txt(0x0031225A) == "lea ecx, [r8 + 0xa]"
      and txt(0x0031225E) == "call 0x329e60",
      "00312170: +0x3A bit, +0x13 byte, +0x0C bits 13/14 -> bits 8/9, OR current kind 10, publish kind 10")
# K3
kinds = {}
for tgt in (0x00321190, 0x00329E60):
    for f, s in sorted(set(c["calls"].get(tgt, ()))):
        kinds[(tgt, s)] = sorted(V.value_at(f, s, "rcx", 1), key=str)
const10 = sorted("%08X" % s for (t, s), v in kinds.items() if ("C", 10) in v)
other = {"%08X" % s: v for (t, s), v in kinds.items() if ("C", 10) not in v}
ok = const10 == ["002FE6E7", "00303088", "00312248", "0031225E"]
ok &= all(v == [("C", 3)] or any(k == "U" and ("shr" in w or "no predecessor" in w) for k, w in v) for v in other.values())
check("K3", ok, "constant-10 sites %s; others %s" % (const10, {k: [x[1] if x[0] != "C" else x[1] for x in v][:2] for k, v in other.items()}))
# K4
t1 = {}
for k in range(0x46):
    t1.setdefault(B + u32i(B + 0x1E3604 + 4 * u8i(B + 0x1E3680 + k)), []).append(k)
ok = txt(0x00301B14) == "movzx r12d, byte ptr [rdx + rdi*2 + 9]" and txt(0x00301B1A) == "movzx ebp, byte ptr [rdx + rdi*2 + 8]" \
    and txt(0x00301B1F) == "movsx esi, word ptr [rdx + rdi*2 + 0xa]" and txt(0x00301B28) == "mov dword ptr [rsp + 0x30], r12d" \
    and txt(0x00301B2D) == "mov dword ptr [rsp + 0x128], ebp" and txt(0x00301B44) == "not r12d" and txt(0x00301B4C) == "and r12d, 1" \
    and txt(0x00301C22) == "cmp eax, 0x37" and txt(0x00301C45) == "cmp edi, 3" and txt(0x00301C48) == "je 0x301c5f" \
    and txt(0x00301C6D) == "cmp ecx, ebp" and txt(0x00301C6F) == "je 0x301db7" \
    and t1.get(0x00303079) == [54, 55] and txt(0x00303081) == "mov rdx, r15" and txt(0x00303084) == "lea ecx, [r8 + 0xa]" \
    and txt(0x0030309C) == "bt eax, esi" and txt(0x0030309F) == "setb cl" and txt(0x00303095) == "mov eax, dword ptr [rsp + 0x64]"
check("K4", ok, "selector opcode 0x36/0x37 mode 3 -> candidate loop -> cases %s at 00303079: bt kind10(candidate), param"
      % t1.get(0x00303079))
# K5
ok = txt(0x002FE6B3) == "mov ecx, 0x4122" and txt(0x002FE6BE) == "cmp ax, 1" and txt(0x002FE6CD) == "mov esi, 0xa" \
    and txt(0x002FE6C4) == "mov ecx, dword ptr [rdi + 0x710]" and txt(0x002FE6D2) == "call 0x31b7e0"
t2 = {}
for k in range(0x36):
    t2.setdefault(B + u32i(B + 0x1DE77C + 4 * u8i(B + 0x1DE790 + k)), []).append(0x4122 + k)
ok &= 0x4122 in t2.get(0x002FE72D, []) and 0x4123 in t2.get(0x002FE738, []) and txt(0x002FE732) == "bts r9d, ebx" \
    and txt(0x002FE73D) == "btr r9d, ebx" and txt(0x002FE68D) == "movsx ebx, word ptr [rcx + 2]"
check("K5", ok, "order 0x4122 = bts / 0x4123 = btr of the param bit in kind 10 of unit 0031B7E0([+0x710])")
# K6 - shipped data
bp = open(os.path.join(WORK, "repos-2d/vbf/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin"), "rb").read()
sec = struct.unpack_from("<I", bp, 0x20)[0]
cnt, stride, first = struct.unpack_from("<III", bp, sec + 4)
gam = sum(1 for r in range(cnt) for k in range(3)
          if struct.unpack_from("<H", bp, sec + first + stride * r + 8 + 2 * k)[0] >> 8 in (0x36, 0x37))
u32 = lambda bb, o: struct.unpack_from("<I", bb, o)[0]
u16 = lambda bb, o: struct.unpack_from("<H", bb, o)[0]
s16 = lambda bb, o: struct.unpack_from("<h", bb, o)[0]
sets = recs = 0
bits = collections.Counter()
dyn10 = 0
acts = collections.Counter()
for f in sorted(glob.glob(os.path.join(WORK, "repos-3f/ard/ard/*.ard"))):
    bb = open(f, "rb").read()
    s1 = u32(bb, 0x14)
    if not s1:
        continue
    n = u16(bb, s1)
    so = [u32(bb, s1 + 4 + 4 * i) for i in range(n + 1)]
    for k in range(n):
        base = s1 + so[k]
        sets += 1
        for rr in range(sum(bb[base:base + 12])):
            r = base + 0x20 + 24 * rr
            recs += 1
            a = u16(bb, r)
            if a in (0x4122, 0x4123):
                acts[s16(bb, r + 2)] += 1
            if a in (0x4149, 0x4155, 0x4156, 0x4157) and u16(bb, r + 6) >> 12 == 10:
                dyn10 += 1
            for e in range(3):
                o = r + 6 + 6 * e
                opd, opw, prm = u16(bb, o), u16(bb, o + 2), s16(bb, o + 4)
                if opd and opw >> 8 in (0x36, 0x37):
                    if opw & 0xFF == 3:
                        bits[prm] += 1
                    elif opd >> 12 == 10:
                        dyn10 += 1
check("K6", (cnt, stride) == (256, 0x20) and gam == 0 and (sets, recs) == (1422, 50050) and dyn10 == 0
      and set(bits) == set(range(0, 17)) | {25, 26, 27, 28, 31} and sum(bits.values()) == 6140,
      "player gambit rows with 0x36/0x37: %d; .ard %d sets / %d records: mode-3 tests %d, bits %s; dynamic kind 10: %d; "
      "0x4122/0x4123 bits %s" % (gam, sets, recs, sum(bits.values()), dict(sorted(bits.items())), dyn10, dict(sorted(acts.items()))))
print("FAILS %d" % fails)
