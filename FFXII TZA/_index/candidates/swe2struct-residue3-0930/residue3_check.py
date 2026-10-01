"""residue3_check.py - three single residues (SWE2-STRUCT for OPUS, 2026-09-30). Static, the certified image, kit retool.py and
structflow.py. Run: python -B residue3_check.py   (FAILS 0)

  P1-P9   FCP section 8: who reads the runtime copy whose offset is kept at render record +0x300 (batch-12 proposed row P1)
  G1-G9   the table registry: the byte 0055CD40 copies into the view's +0x558 under +0x570 bit 10 - its source, its values,
          and whether the signed index can reach -1 (slot 50, 0x02EBF198) through that copy
  W1-W9   MS-4: who sends the field-time map container [02B47760] message 0x20

Every census carries a positive control: P3 (the initialiser's own +0x300 write), P6 (structflow finds the known header
reads), G6 (the two known +0x558 writers), W8 (the message-14 census reproduces ms4_check M5's two sites).
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
os.chdir(KIT)          # retool's helpers resolve some inputs against the kit folder
import retool as T  # noqa: E402
import structflow as S  # noqa: E402

R, SZ, SC = T.R, T.sizes(), T.scan()
BASE = 0x00120000
FAILS = 0


def check(cid, ok, detail):
    global FAILS
    FAILS += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", cid, detail))


def ins(a):
    return next(R.md.disasm(R.at(a, 16), a, 1))


def txt(a):
    i = ins(a)
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def rip(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)       # the displacement's sign is applied
    return i.address + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1) if m else None


def ript(a):
    return rip(ins(a))


def pins(table):
    """table: [(addr, regex)] - every instruction must match its regex exactly (re.fullmatch)"""
    bad = [(a, txt(a)) for a, rx in table if not re.fullmatch(rx, txt(a))]
    return not bad, bad


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def callers(f):
    return sorted(SC["calls"].get(f, ()), key=lambda x: x[1])


def riprefs(f):
    return sorted(SC["refs"].get(f, ()))


def u32(a):
    return struct.unpack("<I", R.at(a, 4))[0]


def jt(table, idx_table, n):
    """MSVC two-level jump table: (id - 1) -> byte index -> dword RVA"""
    if idx_table is None:
        return {i + 1: BASE + u32(table + 4 * i) for i in range(n)}
    idx = R.at(idx_table, n)
    return {i + 1: BASE + u32(table + 4 * idx[i]) for i in range(n)}


def calls_between(f, lo, hi):
    return [x for x in body(f) if lo <= x.address < hi and x.mnemonic == "call"]


ALL = None


def all_bodies():
    global ALL
    if ALL is None:
        ALL = []
        for f, n in sorted(SZ.items()):
            d = R.at(f, n)
            if not d:
                continue
            try:
                ALL.append((f, list(R.md.disasm(d, f))))
            except Exception:
                pass
    return ALL


def msg_sends(ID):
    """every call whose rdx or r8 is a lea of a stack slot whose last dword store before the call is ID (either order, a
    30-instruction window cut at the previous call, the register not rewritten after the lea)"""
    out = []
    for f, il in all_bodies():
        for k, c in enumerate(il):
            if c.mnemonic not in ("call", "jmp"):
                continue
            if c.mnemonic == "jmp" and c.op_str.startswith("0x") and f <= int(c.op_str, 16) < f + SZ[f]:
                continue
            win = il[max(0, k - 30):k]
            for j in range(len(win) - 1, -1, -1):
                if win[j].mnemonic == "call":
                    win = win[j + 1:]
                    break
            for reg, r32 in (("rdx", "edx"), ("r8", "r8d")):
                lea = [x for x in win if x.mnemonic == "lea" and x.op_str.startswith(reg + ", [r") and "rip" not in x.op_str]
                if not lea:
                    continue
                slot = lea[-1].op_str.split(", ", 1)[1]
                after = win[win.index(lea[-1]) + 1:]
                if any((x.op_str.startswith(reg + ",") or x.op_str.startswith(r32 + ",")) and x.mnemonic not in ("cmp", "test")
                       for x in after):
                    continue
                st = [x for x in win if x.mnemonic == "mov" and x.op_str.startswith("dword ptr " + slot + ",")]
                if st:
                    v = st[-1].op_str.rsplit(", ", 1)[1]
                    if v.startswith("0x") and int(v, 16) == ID:
                        out.append((f, st[-1].address, c.address, "%s %s" % (c.mnemonic, c.op_str)))
    return out


def static_msgs(ID):
    """every lea of an image address whose first dword is ID, with a call or jmp within the next five instructions, where the
    lea loads rdx or r8 (the message argument of a procedure call or of a walker)"""
    out = []
    for f, il in all_bodies():
        for k, i in enumerate(il):
            if i.mnemonic != "lea" or not (i.op_str.startswith("rdx, [rip") or i.op_str.startswith("r8, [rip")):
                continue
            t = rip(i)
            if t is None or not (0x00800000 <= t < 0x02100000):
                continue
            d = R.at(t, 4)
            if d and struct.unpack("<I", d)[0] == ID and any(c.mnemonic in ("call", "jmp") for c in il[k + 1:k + 6]):
                out.append((f, i.address, t))
    return out


# ============================================================================================ P: FCP section 8's copy
# P1 the copy and its offset
ok, bad = pins([(0x0041F5AB, r"mov ecx, dword ptr \[r14 \+ 0x2fc\]"), (0x0041F5B2, r"call 0x20e600"), (0x0041F5BA, r"call 0x3ab7f0"),
                (0x0041F5BF, r"add eax, ebp"), (0x0041F5C1, r"mov dword ptr \[r14 \+ 0x300\], ebp"), (0x0041F5CE, r"call 0x3e6d10"),
                (0x0041F5D9, r"call 0x3e6cf0"), (0x0041F5E7, r"call 0x861eba"), (0x0041F5EC, r"movsx eax, word ptr \[r14\]"),
                (0x0041F5F3, r"mov dword ptr \[rdi \+ 8\], eax"), (0x0041F5F6, r"call 0x51d220"),
                (0x0041F5FD, r"mov dword ptr \[r14 \+ 0x300\], 0"),
                (0x003E6D1C, r"movzx eax, word ptr \[rdx \+ 0x10\]"), (0x003E6D2F, r"imul eax, ecx, 0x1d0"), (0x003E6D35, r"add eax, 0x10")])
check("P1", ok, "0041F340 copies section 8 (u16[0] x 0x1D0 + 0x10 bytes, 003E6D10) to aux base + ebp, keeps ebp at "
      "record +0x300 (0 when absent, 0041F5FD), stores the record's own word +0 at copy +8 and calls 0051D220 %s" % (bad or ""))

# P2 the four accessors: aux base (0020E600 of +0x2FC, 003AB7F0) + [+0x300], handed on
ok, bad = pins([(0x003E668E, r"test byte ptr \[rax \+ 8\], 1"), (0x003E6694, r"cmp dword ptr \[rbx \+ 0x300\], 0"),
                (0x003E66B0, r"add eax, dword ptr \[rbx \+ 0x300\]"), (0x003E66BF, r"jmp 0x51cde0"),
                (0x003E66F5, r"add eax, dword ptr \[rbx \+ 0x300\]"), (0x003E6704, r"jmp 0x51d310"),
                (0x003E673B, r"add eax, dword ptr \[rbx \+ 0x300\]"), (0x003E6745, r"test edi, edi"), (0x003E6753, r"jmp 0x51db60"),
                (0x003E6758, r"call 0x519720"),
                (0x003E6D65, r"add eax, dword ptr \[rbx \+ 0x300\]"), (0x003E6D70, r"ret"), (0x003E6D71, r"xor eax, eax")])
check("P2", ok, "003E6680 -> 0051CDE0 (gated on payload +8 bit 0), 003E66D0 -> 0051D310, 003E6710 -> 0051DB60 (edx != 0) "
      "or 00519720 (edx == 0), 003E6D40 returns the copy (0 when +0x300 is 0) %s" % (bad or ""))

# P3 census: every 'add r32, dword ptr [reg + 0x300]' in the image, and every caller of the aux-base getter that touches +0x300
adds, aux = [], []
auxcallers = {f for f, _ in callers(0x003AB7F0)}
for f, il in all_bodies():
    for i in il:
        if re.fullmatch(r"add e\w\w, dword ptr \[r\w+ \+ 0x300\]", "%s %s" % (i.mnemonic, i.op_str)):
            adds.append((f, i.address))
    if f in auxcallers and any(re.search(r"\[r\w+ \+ 0x300\]", x.op_str) for x in il):
        aux.append(f)
ok = sorted({f for f, _ in adds}) == [0x003E6680, 0x003E66D0, 0x003E6710, 0x003E6D40] and len(adds) == 4 \
    and sorted(aux) == [0x003E6680, 0x003E66D0, 0x003E6710, 0x003E6D40, 0x0041F340]
check("P3", ok, "image-wide, 'add r32, [reg+0x300]' occurs %d times, all in the four accessors; of the %d callers of 003AB7F0 "
      "the ones that touch +0x300 are %s (control: the initialiser 0041F340, the writer)"
      % (len(adds), len(auxcallers), " ".join("%08X" % f for f in sorted(aux))))

# P4 the accessors' callers
want = {0x003E6680: [(0x00425DC0, 0x00425DEE)], 0x003E66D0: [(0x00425E10, 0x00425E47)],
        0x003E6710: [(0x0041FCF0, 0x0042002A), (0x00520140, 0x0052014B)],
        0x003E6D40: [(0x00421280, 0x004213A1), (0x004213E0, 0x00421552), (0x0042CBF0, 0x0042CE12), (0x0042D050, 0x0042D169)]}
got = {a: callers(a) for a in want}
ok = all(sorted(got[a]) == sorted(want[a]) for a in want) and not any(riprefs(a) for a in want)
check("P4", ok, "callers: " + "; ".join("%08X <- %s" % (a, " ".join("%08X@%08X" % c for c in got[a])) for a in want)
      + "; no rip reference names any accessor")

# P5 what the eight call sites do with it
ok, bad = pins([(0x00425DD0, r"mov eax, dword ptr \[rdx \+ 0x48800\]"), (0x00425DFA, r"movsx eax, word ptr \[rbx \+ rdx \+ 4\]"),
                (0x00425DC4, r"call 0x51d1d0"), (0x00425E3E, r"test byte ptr \[rcx \+ 0x290\], 2"),
                (0x0041FFFD, r"mov ebx, 1"), (0x0042001D, r"mov edx, ebx"),
                (0x00520144, r"movzx edx, word ptr \[rdx \+ 2\]"), (0x00520148, r"and edx, 1"),
                (0x0042CE21, r"movss xmm1, dword ptr \[rdi \+ 0x49c\]"), (0x0042CE2C, r"call 0x51dbe0"),
                (0x0042D173, r"movss xmm1, dword ptr \[rbx \+ 0x49c\]"), (0x0042D17E, r"call 0x51dbe0"),
                (0x004213B9, r"test byte ptr \[rdi \+ 0x284\], 0x20"), (0x004213C0, r"mov edx, 4"), (0x004213C7, r"mov edx, 6"),
                (0x004213CF, r"call 0x51d2f0"),
                (0x0042155C, r"test dword ptr \[rsi \+ 0x284\], 0x1000000"), (0x00421569, r"mov edx, 9"), (0x00421570, r"mov edx, 8"),
                (0x00421575, r"call 0x51d2f0"),
                (0x0051D2F2, r"and dl, 3"), (0x0051D2F5, r"shr eax, 2"), (0x0051D2F8, r"and al, byte ptr \[rcx \+ 7\]"),
                (0x0051D2FB, r"or al, dl"), (0x0051DBE0, r"movss dword ptr \[rcx \+ 0xc\], xmm1"), (0x00519720, r"mov byte ptr \[rcx \+ 6\], 0")])
check("P5", ok, "00425DC0 / 00425E10 walk the live render-record list (head +0x48800, next +4; 00425E10 skips +0x290 bit 1); "
      "the promoter path 0041FCF0 passes 1 and command 0x1F's handler 00520140 passes word+2 & 1; the LOD updates store record "
      "+0x49C at copy +0xC (0051DBE0); 00421280 / 004213E0 merge codes 4/6 and 8/9 into copy +7 (0051D2F0) %s" % (bad or ""))

# P6 structflow from each consumer with the copy in rcx: no escape, no hand-off, and the header / record fields it uses
CONS = (0x0051CDE0, 0x0051D310, 0x0051DB60, 0x00519720, 0x0051DBE0, 0x0051D2F0, 0x0051D220)
res = {}
for root in CONS:
    F = S.Flow(fields=set(range(0x1D0)), depth=1, stride=0x1D0)
    F.enqueue(root, {"rcx": {"B"}}, 1)
    while F.q:
        f = F.q.pop()
        d, e = F.entry[f]
        F.walk(f, e, d)
    hdr = sorted({(h[4], h[2]) for h in (F.hits | F.unk) if h[3] == "B"})
    rec = sorted({(h[4], h[2]) for h in (F.hits | F.unk) if h[3] == "E0" and h[0] == root and h[5] <= 16
                  and not re.search(r"\[rax", h[6])})
    res[root] = (F.esc, F.handoffs, F.indirect, hdr, rec, sorted(F.entry))
hand = {(r, h[1], h[2]) for r in CONS for h in res[r][1]}
noesc = all(not v[0] and not v[2] for v in res.values()) and hand == {(0x0051DB60, 0x0051DBB5, 0x00861EC0)}
h = {r: {o for o, _ in res[r][3]} for r in CONS}
ok = noesc and {0, 2, 6, 7, 8} <= h[0x0051CDE0] and {0, 2, 6, 7, 8} <= h[0x0051D310] and h[0x0051DBE0] == {0xC} \
    and h[0x0051D2F0] == {7} and h[0x00519720] == {6} and h[0x0051D220] == {6} and {0, 2, 6} <= h[0x0051DB60]
check("P6", ok, "no escape or indirect call carries the copy in any of the seven, and the one hand-off is 0051DB60's memset "
      "of a record's history (0051DBB5 -> 00861EC0); header offsets used: "
      + "; ".join("%08X %s" % (r, ",".join("%X%s" % (o, k) for o, k in res[r][3])) for r in CONS))
print("      record offsets (r/w) in 0051D310: %s" % " ".join("%X%s" % x for x in res[0x0051D310][4]))
print("      record offsets (r/w) in 0051DB60: %s" % " ".join("%X%s" % x for x in res[0x0051DB60][4]))

# P7 the per-frame update 0051D310: gate, bone-anchored point, a 16-deep history
ok, bad = pins([(0x0051D337, r"cmp byte ptr \[rcx \+ 6\], 0"), (0x0051D341, r"movzx eax, byte ptr \[rcx \+ 7\]"),
                (0x0051D34B, r"test al, 1"), (0x0051D373, r"lea r12d, \[r14 \+ 0x10\]"),
                (0x0051D390, r"movzx ecx, word ptr \[rsi \+ 8\]"), (0x0051D3AA, r"imul rdi, rax, 0x740"),
                (0x0051D3BF, r"movaps xmm0, xmmword ptr \[rbx \+ 0x1a0\]"), (0x0051D3CC, r"mov dword ptr \[rsp \+ 0x3c\], 0x3f800000"),
                (0x0051D404, r"mov edx, dword ptr \[rbx \+ 0xc\]"), (0x0051D407, r"call 0x421d70"), (0x0051D424, r"call 0x4220f0"),
                (0x0051D43B, r"mov eax, dword ptr \[rbx\]"), (0x0051D44B, r"cmovg eax, r12d"), (0x0051D455, r"mov dword ptr \[rbx\], eax"),
                (0x0051D929, r"movups xmmword ptr \[rbx \+ 0xa0\], xmm0"), (0x0051DAFA, r"mov dword ptr \[rbx \+ 0x10\], eax"),
                (0x0051DAFD, r"add rbx, 0x1d0")])
ok = ok and ript(0x0051D345) == 0x02CA8428 and ript(0x0051D394) == 0x022C6F28
check("P7", ok, "0051D310 runs while copy +6 != 0 and (+7 | [02CA8428]) bit 0 is clear; per 0x1D0 record it maps the point "
      "+0x1A0 (w = 1) through bone id +0xC of the owning render record (+8 indexes 022C6F28), counts +0 up to 16, rewrites the "
      "rows +0xA0..+0x19F and +0x10 %s" % (bad or ""))

# P8 the draw 0051CDE0: gate, two packets submitted at once through 00540C70 (its only caller)
ok, bad = pins([(0x0051CE5F, r"cmp byte ptr \[rbx \+ 6\], 0"), (0x0051CE69, r"movzx eax, byte ptr \[rbx \+ 7\]"),
                (0x0051CE73, r"test r14b, al"), (0x0051CFD4, r"call 0x540c70"), (0x0051D0F4, r"call 0x3e5770"),
                (0x0051D131, r"mulss xmm0, dword ptr \[rdi \+ 0x1c0\]"), (0x0051D146, r"movss xmm0, dword ptr \[rbx \+ 0xc\]"),
                (0x0051D169, r"lea edx, \[r8 \+ 0x1e\]"), (0x0051D17D, r"call 0x540c70"), (0x0051D187, r"add rdi, 0x1d0"),
                (0x003E5770, r"movss xmm0, dword ptr \[rcx \+ 0x260\]"), (0x003E5778, r"mulss xmm0, dword ptr \[rcx \+ 0x160\]"),
                (0x003E5780, r"mulss xmm0, dword ptr \[rcx \+ 0x26c\]")])
ok = ok and ript(0x0051CE6D) == 0x02CA8428 and ript(0x0051CE81) == 0x02AEC180 and ript(0x0051CFDD) == 0x02AEC2D0 \
    and sorted({f for f, _ in callers(0x00540C70)}) == [0x0051CDE0] and txt(0x00425DC4) == "call 0x51d1d0" \
    and ript(0x0051D1D6) == 0x02064E30 and ript(0x0051D1F2) == 0x02CA8430 and ript(0x0051D206) == 0x02CA8438 \
    and txt(0x0051D201) == "call 0x2d7e00" and txt(0x0051D219) == "jmp 0x2d7e00"
check("P8", ok, "0051CDE0 draws while +6 != 0 and (+7 | [02CA8428]) bit 1 is clear: template 02AEC180 (0x15 units), then per "
      "record the template 02AEC2D0 (0x1E units) with the record's first 0x1A0 bytes spliced in at +0x10, scaled by "
      "003E5770 (+0x260 x +0x160 x +0x26C of the render record), record +0x1C0 and copy +0xC; 00540C70's only caller; "
      "00425DC0 first binds 02CA8430 / 02CA8438 (0051D1D0) %s" % (bad or ""))

# P9 the one-time init and the reset
ok, bad = pins([(0x0051D226, r"cmp dword ptr \[rip \+ 0x278b1ff\], 0"), (0x0051D284, r"call 0x184140"), (0x0051D2AF, r"call 0x1837a0"),
                (0x0051D2C0, r"mov byte ptr \[rbx \+ 6\], 0"), (0x0051DB7C, r"mov word ptr \[rcx \+ 6\], 1"),
                (0x0051DB97, r"mov dword ptr \[rbx \+ 0x14\], 0x3f800000"), (0x0051DBA0, r"mov dword ptr \[rbx\], ebp"),
                (0x0051DBA8, r"mov dword ptr \[rbx \+ 0x1c4\], 1"), (0x0051DBB2, r"mov dword ptr \[rbx \+ 0x10\], ebp"),
                (0x0051DBA2, r"mov r8d, 0x100"), (0x0051DBB5, r"call 0x861ec0")])
ok = ok and ript(0x0051D270) == 0x01F2B340 and ript(0x0051D295) == 0x02CA8430 and ript(0x0051D2B9) == 0x02CA8438 \
    and R.at(0x01F2B34B, 2) == b"\x06\x06"
check("P9", ok, "0051D220 builds the two resources 02CA8430 / 02CA8438 once (flag 02CA842C) from the image block 01F2B340 "
      "(1 << 6 by 1 << 6), and leaves +6 = 0; 0051DB60 enables (+6 = 1, +7 = 0) and resets each record: +0 = 0, +0x10 = 0, "
      "+0x14 = 1.0, +0x1C4 = 1, the 0x100-byte history +0xA0 zeroed %s" % (bad or ""))

# ============================================================================================ G: the registry's +0x558 copy
# G1 the copy and its owner
ok, bad = pins([(0x0055CDE6, r"mov rsi, qword ptr \[rdx \+ 8\]"), (0x0055CE95, r"mov rax, qword ptr \[rsi\]"),
                (0x0055CE98, r"mov qword ptr \[rdi \+ 0x130\], rax"), (0x0055CEB2, r"mov eax, dword ptr \[rdx \+ 0x10c\]"),
                (0x0055CEB8, r"shl eax, 8"), (0x0055CEC1, r"and eax, 0x400"), (0x0055CEC6, r"xor dword ptr \[rdi \+ 0x570\], eax"),
                (0x0055CF73, r"bt ecx, 0xa"), (0x0055CF79, r"movzx eax, byte ptr \[rdx \+ 0x108\]"),
                (0x0055CF80, r"mov byte ptr \[rdi \+ 0x558\], al"), (0x0055C6B2, r"mov qword ptr \[rsp \+ 0x20\], rcx"),
                (0x0055C6E5, r"mov ecx, 0x580"), (0x0055C6EA, r"call 0x244f50"), (0x005614E4, r"mov rcx, rdi"),
                (0x005614E7, r"call 0x55c690")])
cj = jt(BASE + 0x43DB2C, None, 0x17)
ok = ok and cj[1] == 0x0055CDE6 and riprefs(0x0055CD40) == [(0x0055C690, 0x0055C6D1, "lea")] \
    and callers(0x0055C690) == [(0x00561390, 0x005614E7)]
check("G1", ok, "the board view 0055CD40 (created only by 0055C690, whose only caller is 00561390's arm 0x10) takes its owner "
      "from the creation parameter, copies owner +0x10C bit 2 to +0x570 bit 10 and, under it, owner byte +0x108 to +0x558 %s" % (bad or ""))

# G2 the owner (00561390) and who creates it
ok, bad = pins([(0x0056153C, r"mov rbx, qword ptr \[rdx \+ 8\]"), (0x005615B1, r"mov ecx, dword ptr \[rbx \+ 8\]"),
                (0x005615B4, r"shl ecx, 2"), (0x005615B9, r"and ecx, 4"), (0x005615BE, r"mov dword ptr \[rdi \+ 0x10c\], ecx"),
                (0x005615C6, r"movzx eax, byte ptr \[rbx \+ 0x18\]"), (0x005615CA, r"mov byte ptr \[rdi \+ 0x108\], al"),
                (0x00561322, r"movsx eax, r8b"), (0x00561332, r"mov dword ptr \[rsp \+ 0x38\], eax"),
                (0x00561354, r"mov dword ptr \[rsp \+ 0x28\], edx"),
                (0x005590D4, r"movzx r8d, byte ptr \[rdi \+ 0xdc\]"), (0x005590E3, r"call 0x561300"),
                (0x00560C90, r"mov r8b, 0xff"), (0x00560C93, r"xor edx, edx"), (0x00560C98, r"call 0x561300")])
ok = ok and riprefs(0x00561390) == [(0x00561300, 0x00561358, "lea")] \
    and sorted(callers(0x00561300)) == [(0x00558FB0, 0x005590E3), (0x00560910, 0x00560C98)]
check("G2", ok, "the owner 00561390 (created only by 00561300) takes +0x108 = parameter byte +0x18 and +0x10C bit 2 = "
      "parameter +8 bit 0; 00561300 is called by 00558FB0 (byte = its +0xDC) and by 00560910 (byte 0xFF, bit 0) %s" % (bad or ""))

# G3 the owner's bit 2 is set later without touching +0x108; its destroy arm forwards the byte
bj = {0x12: 0x00561403}
ok, bad = pins([(0x0055D641, r"call 0x323630"), (0x0055D646, r"cmp al, 0xff"), (0x0055D68C, r"or dword ptr \[rax \+ 0x10c\], 4"),
                (0x0055D6B2, r"call 0x244f00"), (0x0055D6D6, r"call 0x244f00"),
                (0x0055F4CB, r"or dword ptr \[rax \+ 0x10c\], 4"), (0x0055F4F1, r"call 0x244f00"), (0x0055F50D, r"call 0x244f00"),
                (0x005613AE, r"sub ecx, 1"), (0x005613B7, r"sub ecx, 0xe"), (0x005613C0, r"sub ecx, 1"), (0x005613C9, r"sub ecx, 2"),
                (0x005613CC, r"je 0x561403"), (0x00561424, r"test byte ptr \[rdi \+ 0x10c\], 1"),
                (0x00561460, r"test byte ptr \[rdi \+ 0x10c\], 4"), (0x0056148C, r"movzx r8d, byte ptr \[rdi \+ 0x108\]"),
                (0x0056149B, r"shr edx, 2"), (0x0056149E, r"and edx, 1"), (0x005614A1, r"call 0x558f20"),
                (0x00558F42, r"movsx eax, r8b"), (0x00558F6E, r"mov dword ptr \[rsp \+ 0x28\], edx"),
                (0x0055911A, r"mov eax, dword ptr \[rbx \+ 8\]"), (0x00559125, r"and eax, 2"), (0x0055912E, r"movzx eax, byte ptr \[rbx \+ 0x18\]"),
                (0x00559134, r"mov byte ptr \[rdi \+ 0xdc\], al"), (0x00559076, r"test byte ptr \[rdi \+ 0xe0\], 2"),
                (0x00560C81, r"mov r8b, 0xff"), (0x00560C84, r"xor edx, edx"), (0x00560C89, r"call 0x558f20")])
aj = jt(BASE + 0x4394E4, None, 0x14)
ok = ok and aj[1] == 0x005590EF and aj[0x12] == 0x00558FF0 and riprefs(0x00558FB0) == [(0x00558F20, 0x00558F72, "lea")] \
    and sorted(callers(0x00558F20)) == [(0x00560910, 0x00560C89), (0x00561390, 0x005614A1)]
check("G3", ok, "the view sets owner bit 2 when the character has no board (0055D646, 0055F4CB) and destroys itself and the "
      "owner; the owner's destroy arm (id 0x12) then creates the picker panel 00558FB0 with its +0x108 byte and bit 1; the panel's "
      "destroy arm (0x12) recreates the owner from its +0xDC when its +0xE0 bit 1 is set %s" % (bad or ""))

# G4 the board picker (00557DB0, a child of the panel) reports its cursor; 0xFF is reported with the bit cleared
ok, bad = pins([(0x0055833A, r"mov rax, qword ptr \[rdx \+ 8\]"), (0x0055833E, r"sub rax, 0x8000"), (0x00558354, r"cmp rax, 1"),
                (0x005583BE, r"cmp byte ptr \[rdi \+ 0x10\], 0xff"), (0x005583CB, r"or dword ptr \[rax \+ 0xe0\], 2"),
                (0x005583D9, r"movzx eax, byte ptr \[rdi \+ 0x10\]"), (0x005583DD, r"mov byte ptr \[rcx \+ 0xdc\], al"),
                (0x00558401, r"and dword ptr \[rax \+ 0xe0\], 0xfffffffd"), (0x0055840F, r"mov byte ptr \[rax \+ 0xdc\], 0xff"),
                (0x00557CE4, r"or r8, 0xffffffffffffffff"), (0x00557CE8, r"mov edx, 0x8002"), (0x00557CF0, r"call 0x247510"),
                (0x00557D64, r"mov edx, 0x8002"), (0x00557D7D, r"movsx r8, byte ptr \[rbx \+ 0x358\]"),
                (0x00247523, r"mov dword ptr \[rsp \+ 0x20\], 0xc"), (0x00247530, r"mov qword ptr \[rsp \+ 0x30\], r8"),
                (0x00557C50, r"cmp cl, 0xb"), (0x00557C60, r"mov byte ptr \[rbx \+ 0x358\], 0"), (0x00557C88, r"test cl, cl"),
                (0x00557C97, r"mov byte ptr \[rbx \+ 0x358\], 0xb"), (0x00558119, r"cmp byte ptr \[rbp \+ 0x358\], 0xff"),
                (0x00558122, r"mov byte ptr \[rbp \+ 0x358\], 0")])
ok = ok and riprefs(0x00557DB0) == [(0x00557AE0, 0x00557B21, "lea")] and callers(0x00557AE0) == [(0x00558FB0, 0x0055937C)] \
    and callers(0x00557B90) == [(0x00557DB0, 0x00558288)]
check("G4", ok, "the picker 00557DB0 (created only by the panel, 0055937C) answers {0xC, 0x8002, value} from its input "
      "handler with its cursor +0x358 (wraps 11 <-> 0; 0xFF is normalised to 0 at start) or with -1 on the no-board cancel; "
      "its 0x8002 arm writes the panel's +0xDC and sets +0xE0 bit 1 only for a value other than 0xFF %s" % (bad or ""))

# G5 the chain's own stores: census of non-stack stores to +0xDC / +0xE0 / +0x108 / +0x10C in the licence UI band
chain = []
for f, il in all_bodies():
    if not (0x00557000 <= f < 0x00562000):
        continue
    for i in il:
        t = "%s %s" % (i.mnemonic, i.op_str)
        if re.fullmatch(r"(mov|or|and|xor) (byte|word|dword) ptr \[r(?!sp|bp)\w+ \+ 0x(dc|108|10c|e0)\], .*", t):
            chain.append((f, i.address, t))
PANEL = [0x005583CB, 0x005583DD, 0x00558401, 0x0055840F, 0x00559128, 0x00559134, 0x005593DA]
OWNER = [0x0055D56F, 0x0055D5C8, 0x0055D67F, 0x0055D68C, 0x0055F4BD, 0x0055F4CB, 0x005615A5, 0x005615BE, 0x005615CA]
OTHER = [0x00559B06, 0x00559B0D, 0x00559D71, 0x0055C7B9, 0x00560B74]
ok = sorted(a for _, a, _ in chain) == sorted(PANEL + OWNER + OTHER) and txt(0x005599DE) == "mov rbx, rcx"     and riprefs(0x005599D0) == [(0x00559860, 0x005598A8, "lea")] and txt(0x0055C7B9) == "mov dword ptr [rcx + 0xdc], 1"     and txt(0x00560B57) == "mov rdx, qword ptr [rbx + 0xc0]"
check("G5", ok, "%d non-stack stores in the licence-UI band 00557000-00562000 touch +0xDC/+0xE0/+0x108/+0x10C: the panel's "
      "(own, or the picker's through +0xC0) %s; the owner's (own, or the view's through +0x130) %s; other objects %s (005599D0's "
      "own widget; a dword 1 at [[0209AC30]+0x118]+0xDC, never 0xFF; the screen's parent [screen+0xC0])"
      % (len(chain), " ".join("%08X" % a for a in PANEL), " ".join("%08X" % a for a in OWNER), " ".join("%08X" % a for a in OTHER)))

# G6 census: every store covering +0x558 or +0x559, image-wide (control: the two known writers)
cov = []
for f, il in all_bodies():
    for i in il:
        if i.mnemonic in ("cmp", "test", "lea", "nop", "bt") or not i.operands or i.operands[0].type != 3:
            continue
        m = i.operands[0].mem
        if m.base == 41 or m.index:
            continue
        if m.disp <= 0x559 and m.disp + i.operands[0].size > 0x558 and m.disp > 0x400:
            cov.append((f, i.address, "%s %s" % (i.mnemonic, i.op_str)))
lic = [x for x in cov if 0x00550000 <= x[0] < 0x00570000]
ok = [(f, a) for f, a, _ in lic] == [(0x0055B3F0, 0x0055B44B), (0x0055B3F0, 0x0055B45C), (0x0055B3F0, 0x0055B48A),
                                      (0x0055CD40, 0x0055CF80)]
check("G6", ok, "%d stores in %d functions cover +0x558/+0x559 image-wide; the ones in the 0055-0056 UI band are %s; the rest are "
      "in %s" % (len(cov), len({f for f, _, _ in cov}), " ".join("%08X" % a for _, a, _ in lic),
                 " ".join(sorted({"%08X" % f for f, _, _ in cov if not 0x00550000 <= f < 0x00570000}))))

# G7 the guard: the copy path reaches 0055B3F0 with no call in between, and 0055B3F0 tests the byte on both paths
between = calls_between(0x0055CD40, 0x0055CF80, 0x0055D105)
ok, bad = pins([(0x0055D105, r"call 0x55b3f0"), (0x0055B417, r"xor ebp, ebp"), (0x0055B429, r"cmp qword ptr \[rdi \+ 0x128\], rbp"),
                (0x0055B436, r"test dword ptr \[rdi \+ 0x570\], 0x400"), (0x0055B440, r"jne 0x55b451"),
                (0x0055B44B, r"mov byte ptr \[rdi \+ 0x558\], al"), (0x0055B451, r"movzx eax, byte ptr \[rdi \+ 0x558\]"),
                (0x0055B458, r"cmp al, 0xff"), (0x0055B45C, r"mov word ptr \[rdi \+ 0x559\], bp"), (0x0055B463, r"jmp 0x55b53f"),
                (0x0055B48A, r"mov byte ptr \[rdi \+ 0x559\], dl"),
                (0x00246620, r"movdqu xmmword ptr \[rsp \+ 0x28\], xmm0"), (0x00246626, r"call 0x861ec0"),
                (0x00244FCD, r"call 0x2465f0"), (0x0055DC46, r"mov rcx, qword ptr \[rcx \+ 0x128\]"),
                (0x0055DC57, r"mov qword ptr \[rbx \+ 0x128\], rdi"), (0x0055DC61, r"call 0x55b3f0")])
ok = ok and not between and sorted(callers(0x0055B3F0)) == [(0x0055CD40, 0x0055D105), (0x0055DBD0, 0x0055DC61)]
check("G7", ok, "no call between the copy 0055CF80 and 0055B3F0 at 0055D105; the widget is zeroed at creation (002465F0 "
      "memset), so +0x128 is null and 0055B3F0 runs; bit 10 skips only the lookup, and 0055B451-0055B463 set the count word "
      "+0x559 to 0 for a 0xFF index on both paths; the rebuild 0055DBD0 frees +0x128 first, so the guard runs again %s" % (bad or ""))

# G8 the reader: the -1 load sits inside the count loop
ok, bad = pins([(0x0055C070, r"movsx ecx, byte ptr \[rbp \+ 0x559\]"), (0x0055C08D, r"test ecx, ecx"), (0x0055C08F, r"jle 0x55c3ae"),
                (0x0055C0A0, r"movsx rax, byte ptr \[rbp \+ 0x558\]"),
                (0x0055C0A8, r"mov rdx, qword ptr \[rdx \+ rax\*8 \+ 0x2d9f1a0\]")])
ok = ok and BASE + 0x2D9F1A0 - 8 == 0x02EBF198 and sorted(callers(0x0055BFF0)) == [(0x0055B560, 0x0055B6BD), (0x0055DD70, 0x0055DD89)]
check("G8", ok, "0055BFF0 reads [0x02EBF1A0 + 8 x idx] only inside the loop of byte +0x559 iterations, so idx = -1 "
      "(0x02EBF198) needs a non-zero count, which the guard never leaves beside 0xFF %s" % (bad or ""))

# G9 the only writers of the count are 0055B3F0's two stores (from G6), and the index's only writers are 0055B44B / 0055CF80
ok = [a for f, a, _ in lic if "0x559" in _] == [0x0055B45C, 0x0055B48A] and [a for f, a, _ in lic if "0x558" in _] == [0x0055B44B, 0x0055CF80]
check("G9", ok, "in the licence UI the count +0x559 is written only by 0055B45C / 0055B48A and the index +0x558 only by "
      "0055B44B / 0055CF80, so after every 0055B3F0 run (index == 0xFF) implies (count == 0), and nothing changes either "
      "before the next run")

# ============================================================================================ W: MS-4, message 0x20
# W1 the framework: child links, the bubble-up and subtree walkers, destroy and activation notices
ok, bad = pins([(0x00248230, r"mov rcx, qword ptr \[rcx \+ 0x18\]"), (0x00248239, r"mov qword ptr \[rbx \+ 0x18\], rdx"),
                (0x0024825C, r"mov qword ptr \[rcx \+ 0x20\], rsi"), (0x00248267, r"mov qword ptr \[rdx \+ 0x10\], rbx"),
                (0x00244960, r"cmp qword ptr \[rdx \+ 0x10\], 0"), (0x00244965, r"je 0x248220"),
                (0x00275452, r"mov rbx, qword ptr \[rcx \+ 0x10\]"), (0x0027546E, r"call rax"),
                (0x00275470, r"mov rbx, qword ptr \[rbx \+ 0x10\]"),
                (0x00275405, r"mov rbx, qword ptr \[rcx \+ 0x18\]"), (0x0027540E, r"call rax"), (0x0027541B, r"call 0x2753f0"),
                (0x00275420, r"mov rbx, qword ptr \[rbx \+ 0x20\]"),
                (0x0024505A, r"call rax"), (0x00245064, r"call 0x2473b0"), (0x002473C9, r"call rax"), (0x002473D3, r"call 0x2473b0"),
                (0x00246AE5, r"cmp qword ptr \[rdx \+ 0x10\], 0"), (0x00246AF5, r"call 0x248220"), (0x00246C09, r"call rax")])
m18 = struct.unpack("<II", R.at(0x00915070, 8))
ok = ok and ript(0x00245050) == 0x00915070 and ript(0x002473C2) == 0x00915070 and m18 == (18, 0) \
    and ript(0x00246BFF) == 0x01E0C0E0 and struct.unpack("<I", R.at(0x01E0C0E0, 4))[0] == 14
check("W1", ok, "00248220 appends a child (+0x18 first, +0x20 next, +0x10 parent); 00244960 links only a parentless child; "
      "00275440 sends a message to every ancestor (+0x10 chain); 002753F0 to a widget and its subtree; destroying (00245020) "
      "sends {18} to the widget and every descendant (002473B0); activation (00246AD0) sends {14} %s" % (bad or ""))

# W2 the container's creation message: mode 5, so never the mode-6 arms
ok, bad = pins([(0x003CB45D, r"movdqa xmm0, xmmword ptr \[rip \+ 0x94630b\]"), (0x003CB483, r"movdqu xmmword ptr \[rsp \+ 0x28\], xmm0"),
                (0x003CB489, r"call 0x244f50"), (0x00246726, r"mov rax, qword ptr \[rsi \+ 8\]"),
                (0x0024672F, r"mov rax, qword ptr \[rsi \+ 0x10\]"), (0x003CB6B2, r"movzx eax, byte ptr \[rdx \+ 0x10\]"),
                (0x003CB6B6, r"mov byte ptr \[rdi \+ 0x179d8\], al")])
tmpl = struct.unpack("<QQ", R.at(0x00D11770, 16))
w179d8 = [(f, i.address) for f, il in all_bodies() for i in il
          if re.fullmatch(r"mov byte ptr \[r\w+ \+ 0x179d8\], .*", "%s %s" % (i.mnemonic, i.op_str))]
ok = ok and ript(0x003CB45D) == 0x00D11770 and tmpl == (0, 5) \
    and sorted(w179d8) == [(0x002B7590, 0x002B760C), (0x002BA700, 0x002BA77B), (0x003CB650, 0x003CB6B6)]
check("W2", ok, "003CB440 creates [02B47760] with the message {1, 0, 5} (00D11770 = %s), so its mode +0x179D8 is 5; the "
      "container procedure's only mode store is 003CB6B6 (the other two are in 002B7590 / 002BA700, other containers) %s"
      % (tmpl, bad or ""))

# W3 the container's 0x10 and 0x22 arms
cmap = {}
idx = R.at(BASE + 0x2ABA24, 0x2C)
for i in range(1, 0x2D):
    cmap[i] = BASE + u32(BASE + 0x2AB9EC + 4 * idx[i - 1])
ok, bad = pins([(0x003CB6F6, r"cmp rax, 0x100"), (0x003CB6FE, r"add rax, -0x101"), (0x003CB704, r"cmp rax, 1"),
                (0x003CB70A, r"or word ptr \[rdi \+ 0x179d2\], 2"), (0x003CB714, r"or word ptr \[rdi \+ 0x179d2\], 1"),
                (0x003CB723, r"and al, 3"), (0x003CB725, r"cmp al, 3"), (0x003CB72D, r"cmp byte ptr \[rdi \+ 0x179d8\], 6"),
                (0x003CB763, r"mov dword ptr \[rsp \+ 0x20\], 0x22"), (0x003CB785, r"call rax"),
                (0x003CB7B4, r"mov ecx, 0xc0"), (0x003CB7B9, r"call 0x244f50"), (0x003CB7C1, r"mov rcx, rdi"),
                (0x003CB7C7, r"call 0x244960"), (0x003CB7CC, r"mov rcx, rbx"), (0x003CB7CF, r"call 0x246ac0")])
ok = ok and cmap[0x10] == 0x003CB6F2 and cmap[0x22] == 0x003CB7AA and cmap[0x20] == 0x003CB7DB and cmap[0x23] == 0x003CB78E \
    and ript(0x003CB7AD) == 0x002BA240
check("W3", ok, "container 0x10: code 0x100 sets +0x179D2 bit 0, codes other than 0x100-0x102 set bit 1; once both are set "
      "and the mode is not 6 it sends itself 0x22; 0x22 creates the 0xC0-byte relay 002BA240, links it as its own child "
      "(00244960) and activates it %s" % (bad or ""))

# W4 the relay: activation -> 0x10 -> self-destroy -> {18} -> bubbles {0x20} to its ancestors
rj = {}
ok, bad = pins([(0x002BA256, r"sub r8d, 1"), (0x002BA260, r"sub r8d, 0xd"), (0x002BA266, r"sub r8d, 2"), (0x002BA26C, r"cmp r8d, 2"),
                (0x002BA26A, r"je 0x2ba2b8"), (0x002BA270, r"je 0x2ba289"), (0x002BA264, r"je 0x2ba2d1"),
                (0x002BA28C, r"mov dword ptr \[rsp \+ 0x20\], 0x20"), (0x002BA294, r"lea rdx, \[rsp \+ 0x20\]"),
                (0x002BA29F, r"call 0x275440"), (0x002BA2B8, r"call 0x245020"),
                (0x002BA2D6, r"call 0x249580"), (0x002BA2DB, r"mov edx, 2"), (0x002BA2E6, r"call 0x3c2100"), (0x002BA2EE, r"call 0x249410"),
                (0x002495B7, r"mov qword ptr \[rax \+ 8\], rcx"), (0x003C2149, r"mov dword ptr \[rsp \+ 0x20\], 0x10"),
                (0x003C2169, r"call rax"), (0x00249434, r"cmp word ptr \[rcx \+ 0x1a\], ax"),
                (0x0024945D, r"mov dword ptr \[rsp \+ 0x20\], 0x10"), (0x0024947D, r"call rax")])
check("W4", ok, "the relay 002BA240: on its activation {14} it opens a completion group and either 003C2100 or the group's "
      "close 00249410 delivers {0x10} to it; on 0x10 it destroys itself (00245020); on the resulting {18} it sends {0x20, 0, 0} "
      "through 00275440 to every ancestor - first its parent, the container %s" % (bad or ""))

# W5 the two notices that set bits 0 and 1
ok, bad = pins([(0x003CB498, r"call 0x249580"), (0x003CB4B1, r"call 0x404060"), (0x003CB4B9, r"call 0x249410"),
                (0x003CB4BE, r"mov r8, qword ptr \[rip \+ 0x277c29b\]"), (0x003CB4C5, r"mov edx, 1"), (0x003CB4CC, r"call 0x3bc450"),
                (0x003BC921, r"mov qword ptr \[rbx \+ 0xc0\], rax"), (0x003BC6CD, r"jne 0x3bc735"),
                (0x003BC709, r"mov byte ptr \[rbx \+ 0xc8\], 1"), (0x003BC719, r"mov edx, 0x100"), (0x003BC71E, r"call 0x3bc3e0"),
                (0x003BC403, r"mov dword ptr \[rsp \+ 0x20\], 0x10"), (0x003BC3FB, r"mov qword ptr \[rsp \+ 0x28\], rax"),
                (0x002495ED, r"inc word ptr \[rdi \+ 0x1a\]"), (0x002495FA, r"cmp ax, word ptr \[rdi \+ 0x18\]"),
                (0x00249612, r"mov dword ptr \[rsp \+ 0x20\], 0x10"), (0x00249632, r"call rax")])
ok = ok and ript(0x003CB4BE) == 0x02B47760 and ript(0x003BC4A7) == 0x02B457E0 \
    and sorted({f for f, _ in callers(0x003BC3E0)}) == [0x003BC4E0, 0x003BC9F0]
check("W5", ok, "bit 1: the container's own load group (00404060 into +0x190) delivers {0x10, 0} when its last load "
      "completes (002495C0) or at close if none is pending; bit 0: the loader widget [02B457E0], created beside it with the "
      "container at +0xC0, sends {0x10, 0x100} (003BC3E0) on its first completion %s" % (bad or ""))

# W6 census of message-0x20 sends, image-wide
s20 = msg_sends(0x20)
got = sorted((f, c) for f, _, c, _ in s20)
expect = [(0x00279E20, 0x0027A633), (0x002B6570, 0x002B65FF), (0x002BA040, 0x002BA14E), (0x002BA240, 0x002BA29F),
          (0x00553F40, 0x00554172), (0x00553F40, 0x0055422E), (0x00624C30, 0x00624E67), (0x00797360, 0x007973B2),
          (0x0079B300, 0x0079B729)]
st20 = static_msgs(0x20)
WALKERS = {"call 0x275440", "jmp 0x275440", "call 0x2753f0", "jmp 0x2753f0", "call 0x247490", "call 0x247510", "jmp 0x247510"}
nextcall = []
for f, a, t in st20:
    nxt = next(x for x in list(R.md.disasm(R.at(a, 64), a))[1:] if x.mnemonic in ("call", "jmp"))
    nextcall.append("%s %s" % (nxt.mnemonic, nxt.op_str))
statics_ok = len(st20) == 14 and not (set(nextcall) & WALKERS) and "call rax" not in nextcall \
    and set(nextcall) <= {"call qword ptr [rip + 0x74550f]", "call 0x719460", "call 0x7157a0", "call qword ptr [rax + 0x58]"}
ok = statics_ok and got == expect and ript(0x002B6583) == 0x0209E5C0 and ript(0x002B6601) == 0x0209E5C0 and ript(0x002BA053) == 0x0209E5F0 \
    and txt(0x0027A625) == "mov rcx, rbx" and txt(0x0027A633) == "call 0x2753f0" and txt(0x00279E4F) == "mov rbx, rcx" \
    and riprefs(0x00279E20) == [(0x00276650, 0x002766D1, "lea")] and txt(0x002766D8) == "mov edx, 0x61f0"
check("W6", ok, "%d stack-built 0x20 messages are handed to a call: %s. The relay's bubble (002BA29F) is the one whose path "
      "contains [02B47760]; 002B6570 / 002BA040 message [0209E5C0] / [0209E5F0] directly; 0027A633 broadcasts over the "
      "subtree of its own 0x61F0-byte widget (procedure 00279E20); 00553F40 bubbles from its own widget; the last three are "
      "not widget calls. The %d static structs whose first dword is 0x20 and that are passed in rdx/r8 all go to non-widget "
      "calls (%s): %s"
      % (len(s20), " ".join("%08X@%08X" % x for x in got), len(st20), ", ".join(sorted(set(nextcall))),
         " ".join("%08X@%08X->%08X" % x for x in st20)))

# W7 the container's place in the tree: no parent until its own 0x20 arm activates it (under the layer root, which ignores
# everything but creation), and its only child is the relay
links = []
for f, il in all_bodies():
    for k, i in enumerate(il):
        if i.mnemonic in ("call", "jmp") and i.op_str in ("0x248220", "0x244960", "0x246ad0", "0x246ac0"):
            if f in (0x003CB650, 0x003CB440, 0x003CB410, 0x003CB3D0, 0x003CB3E0, 0x002B6570, 0x002BA040):
                links.append((f, i.address, i.op_str))
ok, bad = pins([(0x002445D0, r"cmp dword ptr \[rdx\], 1"), (0x002445D6, r"jne 0x24460a"), (0x0024460A, r"xor eax, eax"),
                (0x00247D93, r"lea r8, \[rip - 0x37ca\]"), (0x00247D9F, r"mov qword ptr \[rdi\], rbx"),
                (0x00246AC3, r"mov rcx, qword ptr \[rip \+ 0x1e47f5e\]"), (0x003CB7DE, r"call 0x246ac0")])
ok2, bad2 = pins([(0x003CB818, r"mov rdx, rax"), (0x003CB81B, r"mov rcx, rdi"), (0x003CB821, r"call 0x244960"),
                  (0x003CB521, r"cmp r8d, 2"), (0x003CB525, r"je 0x3cb53f"), (0x003CB551, r"mov dword ptr \[rsp \+ 0x20\], 0x2c"),
                  (0x003CB55F, r"call 0x275440")])
ok = ok and ok2 and sorted(links) == [(0x003CB650, 0x003CB7C7, "0x244960"), (0x003CB650, 0x003CB7CF, "0x246ac0"),
                                      (0x003CB650, 0x003CB7DE, "0x246ac0"), (0x003CB650, 0x003CB821, "0x244960")] \
    and ript(0x00246AC3) == 0x0208EA28 and ript(0x00247D20) == 0x0208EA20
check("W7", ok, "in the container's code and in every function naming [02B47760] the only link calls are 003CB7C7 (the relay "
      "under the container), 003CB7CF (the relay activated), 003CB7DE (the container activated under the layer root "
      "[0208EA28], inside its 0x20 arm) and 003CB821 (the preload page under the container, in the same arm); the page "
      "bubbles only {0x2C} (003CB551, on its {18}); the layer roots (procedure 002445D0, built at 00247D9A) handle only id 1 %s"
      % (bad + bad2 or ""))

# W8 control: the same census for id 14 reproduces ms4_check M5's two stack-built sends
s14 = sorted(c for f, _, c, _ in msg_sends(0x0E))
ok = s14 == [0x00292ACD, 0x003CB85F]
check("W8", ok, "control - the census for id 14 finds %s (ms4_check M5: the sends built at 00292AB2 and 003CB835)"
      % " ".join("%08X" % a for a in s14))

# W9 the bits are never cleared in the container, so every later 0x10 notice also re-runs 0x22
clr = [(i.address, "%s %s" % (i.mnemonic, i.op_str)) for i in body(0x003CB650)
       if "0x179d2]" in i.op_str and i.mnemonic in ("and", "xor", "mov", "btr")]
ok = all(a in (0x003CB98B, 0x003CB996, 0x003CB9B9, 0x003CB9C4) for a, _ in clr) and txt(0x003CB992) == "and ax, 0x40" \
    and txt(0x003CB9C0) == "and ax, 0x30"
check("W9", ok, "the container's only other edits of +0x179D2 are the masked xors of bits 6 and 4-5 (%s), so bits 0-1 stay set "
      "and each later {0x10} notice (codes 0x101 / 0x102 included) sends 0x22 again" % " ".join("%08X" % a for a, _ in clr))

print("FAILS %d" % FAILS)
