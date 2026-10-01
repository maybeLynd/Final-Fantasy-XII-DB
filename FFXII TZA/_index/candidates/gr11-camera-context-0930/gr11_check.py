"""gr11_check.py - GR-11: what camera context 0 installs on a focus change, and whether the rest of its +0x6F0 block is
read (OPUS, 2026-09-30). Static, the certified image (kit retool.py).

Contexts: 0x860 bytes at 02097D20; the pose blocks are A = +0x640 (the interpolated output), B = +0x6F0 (the 'from'
pose) and C = +0x7A0 (the 'to' pose), 0xB0 bytes each. The question's "rest of +0x6F0" is B + 0x20..0xAF (+0x710..+0x79F).

K1  the install 0025A180(actor, idx) copies the 0xB0 bytes at [[actor+0xC0]+0x138] + 0x30 (the movement body's placement
    record) into C, then runs the interpolator (out A, from B, to C) and sets word +0x690 = 4.
K2  the interpolator 00259510 reads from / to only at +0x00, +0x04, +0x08 (position) and +0x10, +0x18 (the heading pair)
    and writes out only +0x00..+0x1F.
K3  the blend 00259620 (the field tick: 00259FB0, whose only caller is ActorManager_RunFieldRuntimePass 0025D9E0) walks
    contexts 0 and 1, reads B and C only in their first 0x20 bytes, builds a stack local of which it writes only the first
    0x20 bytes, and copies the local's 0xB0 bytes over B: B + 0x20..0xAF receive stack residue every tick.
K4  the teardown 0025A6A0 does the same: its local is written only as the interpolator's out (+0x00..+0x1F) and is copied
    whole over B (0025A792-0025A7F9); its earlier C -> B copy is replaced by it in the same call.
K5  no rip-relative operand anywhere in .text addresses +0x710..+0x79F of contexts 0 or 1, and the six functions that form
    the base 02097D20 apply no displacement in that window.
K6  every call that receives a pointer into B, from the functions that reference contexts 0 / 1 or form the base, is one of:
    the reset 00259B30's memset 00861EC0, placement init 00380B80 and placement 00380D30, or the interpolator's 'from'
    (00259B30, 0025A180, 0025A6A0); the only other movers of B are the whole-context copies 002593D0 (0 -> 1) and
    00259470 (1 -> 0), both from 00359410; the other base-forming functions hand on only +0x10 and A (00259990) or make
    no call (0025A620).
K7  at the reset 00259B30 (both contexts: r12 = 2, step 0x860) B's tail is the placement routine's working record:
    00380B80 initialises the block (the tail at +0x50..+0xA7) and 00380D30 puts the point on the ground (+0x04) when +0x60 bit 0 is clear.
K8  named limit, first level only: the functions handed the +0x10 view (0x630 bytes) or its +0x2C0 member apply no
    displacement that reaches B (0x6E0 past +0x10, 0x430 past +0x2C0).
Prints PASS/FAIL per check and FAILS n last.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool as T  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
BASE, STRIDE = 0x02097D20, 0x860
A, B, C = 0x640, 0x6F0, 0x7A0
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def body(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return ("%s %s" % (i.mnemonic, i.op_str)).strip()


def ript(i):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
    return i.address + i.size + int(m.group(2), 16) * (1 if m.group(1) == "+" else -1) if m else None


def mems(ins, reg):
    """(address, disp, is_write) of every memory operand based on reg."""
    out = []
    for i in ins:
        for n, op in enumerate(i.operands):
            if op.type == 3 and op.mem.base and i.reg_name(op.mem.base) == reg and i.mnemonic != "lea":
                out.append((i.address, op.mem.disp, n == 0 and len(i.operands) > 1 and i.mnemonic not in ("cmp", "test")))
    return out


callers = lambda f: sorted({x for x, _ in c["calls"].get(f, ())})

# K1
ins = body(0x0025A180)
loads = [i for i in ins if i.mnemonic == "movups" and i.op_str.startswith("xmm") and "[rax" in i.op_str]
stores = [i for i in ins if i.mnemonic == "movups" and i.op_str.startswith("xmmword ptr [r8")]
ok = txt(0x0025A1A2) == "mov rax, qword ptr [rcx + 0xc0]" and txt(0x0025A1B2) == "mov rax, qword ptr [rax + 0x138]" \
    and sorted(i.operands[1].mem.disp for i in loads) == list(range(0x30, 0xE0, 0x10)) \
    and sorted(i.operands[0].mem.disp for i in stores) == list(range(0, 0xB0, 0x10)) \
    and txt(0x0025A1C6) == "lea r8, [rbx + 0x7a0]" and txt(0x0025A1D5) == "lea rdx, [rbx + 0x6f0]" \
    and txt(0x0025A1E0) == "lea rcx, [rbx + 0x640]" and txt(0x0025A25C) == "call 0x259510" \
    and txt(0x0025A266) == "mov word ptr [rbx + 0x690], ax" and callers(0x0025A180) == [0x0025A6A0, 0x00358F90]
check("K1", ok, "0025A180: body +0x30..+0xDF -> C; interpolator(A, B, C); word +0x690 = 4 (callers 0025A6A0, 00358F90)")

# K2
ins = body(0x00259510)
fr = {d for _, d, w in mems(ins, "rbx") if not w} | {d for _, d, w in mems(ins, "rdx") if not w}
to = {d for _, d, w in mems(ins, "rdi") if not w}
out = {d for _, d, w in mems(ins, "rsi") if w}
ok = txt(0x0025952C) == "mov rbx, rdx" and txt(0x00259524) == "mov rdi, r8" and txt(0x00259534) == "mov rsi, rcx" \
    and fr == {0, 4, 8, 0x10, 0x18} and to == {0, 4, 8, 0x10, 0x18} and out and max(out) <= 0x1C \
    and not any(w for _, _, w in mems(ins, "rbx") + mems(ins, "rdi")) \
    and callers(0x00259510) == [0x00259B30, 0x0025A180, 0x0025A6A0]
check("K2", ok, "00259510 reads from %s / to %s, writes out %s" % (sorted(map(hex, fr)), sorted(map(hex, to)), sorted(map(hex, out))))


def local_copy(ins, src_lea, first_store, dst_reg, dst_base):
    """the 11 movups that copy rsp+0x20.. (0xB0) to dst_reg + dst_base .. +0xAF, and no other stack write of rsp+0x40..0xCF."""
    k = [n for n, i in enumerate(ins) if i.address == src_lea][0]
    cp = [i for i in ins[k:k + 40] if i.mnemonic == "movups"]
    ld = sorted(i.operands[1].mem.disp for i in cp if i.op_str.startswith("xmm") and "[rax" in i.op_str)
    st = sorted(i.operands[0].mem.disp - dst_base for i in cp if i.op_str.startswith("xmmword ptr [" + dst_reg))
    other = [i.address for i in ins for n, op in enumerate(i.operands)
             if n == 0 and op.type == 3 and op.mem.base and i.reg_name(op.mem.base) == "rsp" and 0x40 <= op.mem.disp < 0xD0
             and len(i.operands) > 1 and i.mnemonic not in ("cmp", "test")]
    leas = [i.address for i in ins if i.mnemonic == "lea" and re.search(r"\[rsp \+ 0x([4-9a-c][0-9a-f])\]", i.op_str)]
    return ld == list(range(0, 0xB0, 0x10)) and st == list(range(0, 0xB0, 0x10)) and not other and not leas, other + leas


# K3
ins = body(0x00259620)
k = [n for n, i in enumerate(ins) if i.address == 0x00259721][0]
pre = [i for i in ins[:k] for n, op in enumerate(i.operands)
       if n == 0 and op.type == 3 and op.mem.base and i.reg_name(op.mem.base) == "rsp" and len(i.operands) > 1]
pre_ok = all(0x20 <= i.operands[0].mem.disp <= 0x3C for i in pre if i.operands[0].mem.disp >= 0x20)
reads = {d for _, d, w in mems(ins, "rdi") if not w and d != 0x148}
ok_reads = all((B - 0x708) <= d <= (B - 0x708) + 0x1C or (C - 0x708) <= d <= (C - 0x708) + 0x1C for d in reads)
cp_ok, bad = local_copy(ins, 0x00259721, 0x00259742, "rdi", B - 0x708)
ok = ript(ins[[n for n, i in enumerate(ins) if i.address == 0x0025963F][0]]) == BASE + 0x708 \
    and ript(ins[[n for n, i in enumerate(ins) if i.address == 0x00259652][0]]) == BASE + 2 * STRIDE + 0x708 \
    and txt(0x002597B2) == "add rdi, 0x860" and txt(0x002597B9) == "cmp rdi, rbp" and txt(0x00259721) == "lea rax, [rsp + 0x20]" \
    and pre_ok and ok_reads and cp_ok \
    and callers(0x00259FB0) == [0x0025D9E0] and txt(0x00259FBC) == "call 0x259620" and callers(0x00259620) == [0x00259FB0, 0x00343340]
check("K3", ok, "00259620 (field tick 00259FB0 <- 0025D9E0): reads B/C +0x00..+0x1F only (%s), local written only at "
      "rsp+0x20..0x3F, copied whole over B%s" % (" ".join("%+x" % (d + 0x708 - B) for d in sorted(reads)), "" if cp_ok else " BAD %s" % bad))

# K4
ins = body(0x0025A6A0)
cp_ok, bad = local_copy(ins, 0x0025A792, 0x0025A79E, "rbp", 0)
calls_out = [i.address for i in ins if i.mnemonic == "call" and i.op_str == "0x259510"]
ok = txt(0x0025A6BE).startswith("lea rax, [rip") and ript(ins[[n for n, i in enumerate(ins) if i.address == 0x0025A6BE][0]]) == BASE \
    and txt(0x0025A6CB) == "imul r15, rdi, 0x860" and txt(0x0025A6EA) == "lea rbp, [r15 + 0x6f0]" and txt(0x0025A6D2) == "lea rcx, [rsp + 0x20]" \
    and txt(0x0025A777) == "lea rcx, [rsp + 0x20]" and calls_out == [0x0025A6F7, 0x0025A78D] and txt(0x0025A76A) == "call 0x25a180" \
    and cp_ok and callers(0x0025A6A0) == [0x0025A680, 0x0025A690]
check("K4", ok, "0025A6A0: local = interpolator out only, copied whole over B at 0025A792-0025A7F9%s" % ("" if cp_ok else " BAD %s" % bad))

# K5
riprefs, base_fns, win, ctl = set(), set(), [], 0
for f, n in SZ.items():
    try:
        fi = list(R.md.disasm(R.at(f, n), f))
    except Exception:
        continue
    for i in fi:
        t = ript(i)
        if t is None:
            continue
        if BASE <= t < BASE + 2 * STRIDE:
            riprefs.add(f)
            if 0x710 <= (t - BASE) % STRIDE < 0x7A0:
                win.append(i.address)
        if BASE + 2 * STRIDE <= t < BASE + 5 * STRIDE and 0x710 <= (t - BASE) % STRIDE < 0x7A0:
            ctl += 1                                  # control: the same sweep sees slots 2-4's own fields there
        if t == BASE and i.mnemonic == "lea":
            base_fns.add(f)
bwin = [(f, a, d) for f in sorted(base_fns) for r in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r15")
        for a, d, _ in mems(body(f), r) if 0x710 <= d < 0x7A0]
ok = not win and base_fns == {0x002593D0, 0x00259470, 0x00259990, 0x0025A180, 0x0025A620, 0x0025A6A0} and not bwin \
    and 0x0025A180 in base_fns and ctl > 0
check("K5", ok, "control: %d in-window operands in slots 2-4; " % ctl + "no rip-relative operand in +0x710..+0x79F of contexts 0/1 (%d functions reference the two contexts); "
      "base-forming functions %s apply no in-window displacement" % (len(riprefs), " ".join("%08X" % f for f in sorted(base_fns))))

# K6: linear hand-off census over the rip-referencing functions (a pointer into B at a call's rcx / rdx / r8 / r9)
FAM = {r: r for r in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15")}
handoff = set()
for f in sorted(riprefs):
    tag = {}
    for i in body(f):
        ops = [x.strip() for x in i.op_str.split(",")]
        if i.mnemonic == "call":
            for r in ("rcx", "rdx", "r8", "r9"):
                if r in tag and B <= (tag[r] - BASE) % STRIDE < B + 0xB0:
                    handoff.add((f, i.address, i.op_str, r))
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                tag.pop(r, None)
            continue
        if not ops or ops[0] not in FAM:
            continue
        val = None
        if i.mnemonic == "lea":
            t = ript(i)
            if t is not None and BASE <= t < BASE + 2 * STRIDE:
                val = t
            m = re.match(r"\w+, \[(\w+)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]$", i.op_str)
            if t is None and m and m.group(1) in tag:
                d = int(m.group(3), 0) if m.group(3) else 0
                val = tag[m.group(1)] + (-d if m.group(2) == "-" else d)
        elif i.mnemonic == "mov" and len(ops) == 2 and ops[1] in tag:
            val = tag[ops[1]]
        if val is not None:
            tag[ops[0]] = val
        elif i.mnemonic not in ("cmp", "test", "push"):
            tag.pop(ops[0], None)
got = sorted((f, s, r) for f, _, s, r in handoff)
want = [(0x00259B30, "0x259510", "rdx"), (0x00259B30, "0x380b80", "rcx"), (0x00259B30, "0x380d30", "rcx"), (0x00259B30, "0x861ec0", "rcx")]
copies = all(txt(a) == t for a, t in ((0x002593D7, "mov edx, 0x10"), (0x00259477, "mov edx, 0x10")))
ok = got == want and copies \
    and ript(body(0x002593D0)[0]) == BASE + STRIDE and ript(body(0x002593D0)[2]) == BASE \
    and ript(body(0x00259470)[0]) == BASE and ript(body(0x00259470)[2]) == BASE + STRIDE \
    and callers(0x002593D0) == [0x00359410] and callers(0x00259470) == [0x00359410]     and [txt(a) for a in (0x00259A13, 0x00259A1D, 0x00259A28, 0x00259A32)] == ["lea r8, [rdi + 0x640]", "lea rcx, [rdi + 0x10]"] * 2     and not [i for i in body(0x0025A620) if i.mnemonic == "call"]
check("K6", ok, "B handed to %s (00259B30), plus the interpolator 'from' in 0025A180 / 0025A6A0 (K1, K4); whole-context "
      "copies 002593D0 (0 -> 1) and 00259470 (1 -> 0) from 00359410" % ", ".join("%s(%s)" % (s, r) for _, s, r in got))

# K7
ins = body(0x00380B80)
w = sorted({d for _, d, wr in mems(ins, "rcx") if wr})
ok = txt(0x00259C02) == "mov r12d, 2" and txt(0x00259DA3) == "lea r15, [r15 + 0x860]" \
    and ript(body(0x00259B30)[[n for n, i in enumerate(body(0x00259B30)) if i.address == 0x00259BF5][0]]) == BASE + 0x658 \
    and txt(0x00259C67) == "lea rcx, [r15 + 0x98]" and txt(0x00259C6E) == "mov r8d, 0xb0" and txt(0x00259CAE) == "lea rcx, [r15 + 0x98]" \
    and txt(0x00259D5A) == "lea rcx, [r15 + 0x98]" and txt(0x00259D61) == "call 0x380d30" \
    and {0x50, 0x52, 0x60, 0x64, 0x80, 0x98} <= set(w) and max(w) <= 0xA0 \
    and txt(0x00380DC7) == "test byte ptr [rbx + 0x60], 1" and txt(0x00380DD2) == "movss dword ptr [rbx + 4], xmm0" \
    and txt(0x00380DDD) == "call 0x3808a0"
check("K7", ok, "reset 00259B30 (contexts 0 and 1): memset B, 00380B80 writes %s, 00380D30 grounds +0x04 when +0x60 bit 0 is clear"
      % " ".join("%x" % d for d in w))

# K8
lim = {}
for f, cap in ((0x003D9B80, 0x6E0), (0x003D9C40, 0x6E0), (0x003D99B0, 0x6E0), (0x003D9930, 0x6E0), (0x003D9950, 0x6E0),
               (0x0032B8B0, 0x430), (0x0032B880, 0x430)):
    mx = max([op.mem.disp for i in body(f) for op in i.operands
              if op.type == 3 and op.mem.base and i.reg_name(op.mem.base) not in ("rip", "rsp", "rbp")] or [0])
    lim[f] = (mx, cap)
ok = all(mx < cap for mx, cap in lim.values())
check("K8", ok, "first-level displacement bounds (named limit): " + ", ".join("%08X %x<%x" % (f, m, cp) for f, (m, cp) in sorted(lim.items())))
print("FAILS %d" % fails)
