"""check_s29.py - FABLE, 2026-10-03: S-29 item use - reserve, then consume or refund (0030EF20 / 00305640 / 00300280).

Settles, at the bytes of the certified image (73461d08..., base 0x00120000), the claims of section.txt (IU1-IU6):

  K1  raw index: 0030EF20 is called at 00304962 (00304850) and 003073AB (00307300); 00305640 at 00304F38 (00304850),
      003073B9 (00307300), 003132B7 (00313120), 003192B7 (003191B0); 00300280 at 0031063A (003105D0) only. Every .rdata
      hit on the three is a chained-unwind RUNTIME_FUNCTION copy; no 8-byte pointer constant names any of them.
  K2  the refund is reached only through the cancel 003105D0, which is branch-free from its +0x698 gate (003105EF) to the
      refund call; 003105D0's twelve call sites; the unit reset 00236A60 cancels only when flag-word bit 4 is set
      (00236A6F) and otherwise writes +0xDC8 = 0xFFFF (00236AFC) without a refund and never writes +0xE58.
  K3  prepare runs in phase 0 of 00304850 (jump-table slot 0 -> 0030495C -> 00304962); the only byte stores of 0 to
      +0x6B4 are the commit's (0030F814) and the cancel's (003106F2).
  K4  the commit 0030F760 cancels first when its 5th argument is non-zero (0030F776-0030F78A); four of its five call
      sites pass 1; the fifth, the engage auto-attack 003130DC, passes 0, stashes +0xDC8/+0xE58 at 022C1DB0 first, sets
      phase 5 on success and restores on failure; the restore 00308270 moves no item; 00310780 runs the restore before
      the cancel's refund.  K4g: the combo continuation 0030FA00 re-commits with cancelFirst 1 and enters phase 5; the
      only phase-5 stores are 0030FA80 and 003130F2, so neither phase-5 entry prepares.
  K5  00307300's prepare-and-consume arm (003073AB/003073B9) needs its 5th argument == 1 (00307388); its only caller
      passes 0 (00319354 -> 00319362).
  K6  003191B0 consumes once per committed action: first entry only (003191FD), latch +0x700 bit 1 (00319241 test,
      003192BC set), cleared by the commit (0030F7F2) and the cancel (003106C5).
  K7  00304850's consume (00304F38) runs only for a row whose dword +0x0C has bit 30 and an id outside 0xD0..0xF1.
  K8  prepare and refund discard 003008A0's return value.
  K9  the availability arm 003037A0 admits an item action when the free count (query kind 0) is positive OR the unit's own
      +0xDC8 already holds that item; else reason 0x12.
  K10 00313120 calls the consume (003132B7) and neither the prepare nor the refund; its only caller is 003495A0.
  K13 the call sites the crossings subsection and the evidence list cite (gil get/set in all three bodies, the
      setter's clamp and store, the consume's category tail and its two achievement calls, 00316440's counter 0x13).
  K12 00304850's direct call closure (chained .pdata) does not reach 003191B0 or its two callers (a note on the limit).
  K11 executed (Unicorn 2.1.4, original code; emu.py's planted world):
        a. reserve then consume: owned 3 -> 2, reservation {5, 0}; consume clears it with NO inventory call; a later
           refund returns nothing (owned stays 2);
        b. reserve then refund: owned 3 -> 2 -> 3, delta +1 on channel 1, reservation cleared;
        c. reserve at owned 0: the take stores nothing (floor clamp), the reservation is set anyway, and the refund
           makes owned 1;
        d. a refund at owned 99 clears the reservation and stores nothing (the item is gone);
        e. two prepares with no clear between take two and reserve one: a refund leaves owned 2 of 3;
        f. a kind-1 unit: neither prepare nor refund touches the inventory or +0xDC8;
        g. gil: prepare 1000 -> 610 with +0xE58 = 390, refund 610 -> 1000; consume zeroes +0xE58 and returns nothing;
        h. availability: (owned, equipped, +0xDC8) -> reason as K9 states.

Sensitivity controls (each must make a check FAIL; the control PASSES when it does):
  S1  image: consume's 0xFFFF store 003056BA NOPed: K11a must fail (the refund after consume then returns the item).
  S2  image: prepare's `or edx, -1` (0030EFAA) -> `xor edx, edx`: K11b must fail (no take).
  S3  claim: "a refund never returns more than the prepare took", against K11c's execution, must fail.
  S4  image: 00319354 stores 1 instead of 0: K5 must fail.
  S5  image: the engage's phase store 003130F2 writes 0: K3 must fail (a third zero writer of +0x6B4).

Prints FAILS N last.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, disp_sweep, decode_fn  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_OP_REG  # noqa: E402
from unicorn import __version__ as UC_VERSION  # noqa: E402
import emu  # noqa: E402

PREPARE, CONSUME, REFUND, CANCEL, COMMIT = 0x0030EF20, 0x00305640, 0x00300280, 0x003105D0, 0x0030F760
fails = 0
quiet = [False]


def report(tag, ok, text=""):
    global fails
    if not ok:
        fails += 1
    if not quiet[0]:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))
    return ok


def note(s):
    if not quiet[0]:
        print("      " + s)


def ins(img, a):
    return next(img.cs.disasm(img.read(a, 16), a, 1))


def txt(img, a):
    c = ins(img, a)
    return (c.mnemonic + " " + c.op_str).strip()


def linear(img, s, e):
    return list(img.cs.disasm(img.read(s, e - s), s))


def expect(img, table):
    """table {addr: exact text}; returns the list of mismatches"""
    return ["%08X: %r" % (a, txt(img, a)) for a, t in table.items() if txt(img, a) != t]


def chain_records(img):
    """VAs of the RUNTIME_FUNCTION copies inside chained unwind infos (UNW_FLAG_CHAININFO)."""
    po = img.off(img.base + img.exc_rva)
    out = set()
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        ui = img.off(img.base + u)
        if (img.d[ui] >> 3) & 4:
            n = img.d[ui + 2]
            out.add(img.base + u + 4 + ((n + 1) & ~1) * 2)
    return out


def callers(img, va):
    refs, _ = text_refs(img, va)
    return [(r["site"], r["form"]) for r in refs]


# ---------------------------------------------------------------- K1
def k1(img):
    got = {f: callers(img, f) for f in (PREPARE, CONSUME, REFUND)}
    want = {PREPARE: [(0x00304962, "call"), (0x003073AB, "call")],
            CONSUME: [(0x00304F38, "call"), (0x003073B9, "call"), (0x003132B7, "call"), (0x003192B7, "call")],
            REFUND: [(0x0031063A, "call")]}
    for f in got:
        report("K1a.%08X" % f, got[f] == want[f], "callers of %08X: %s" % (f, ["%08X %s" % g for g in got[f]]))
    cr = chain_records(img)
    bad = []
    for f in (PREPARE, CONSUME, REFUND):
        for s, va, kind, v in data_refs(img, f):
            if kind == "va64" or va not in cr:
                bad.append("%s %08X %s" % (s, va, kind))
    report("K1b", not bad, "every .rdata/.data hit on the three is a chained-unwind RUNTIME_FUNCTION copy, no pointer "
                           "constant %s" % bad)


# ---------------------------------------------------------------- K2
def k2(img):
    body = linear(img, 0x003105EF, 0x0031063A)
    jumps = [c for c in body if c.mnemonic.startswith("j")]
    gates = expect(img, {0x003105D0: "test rcx, rcx", 0x003105D3: "je 0x310771",
                         0x003105DE: "cmp qword ptr [rcx + 0x698], 0", 0x003105E9: "je 0x31076c",
                         0x00310605: "call 0x310780", 0x0031063A: "call 0x300280"})
    report("K2a", not jumps and not gates, "003105D0 is branch-free from 003105EF to the refund call 0031063A "
                                           "(%d jumps), behind the null-unit and null-+0x698 gates %s" % (len(jumps), gates))
    sites = [s for s, f in callers(img, CANCEL)]
    want = [0x00236A77, 0x002FF9C7, 0x0030014D, 0x00300E61, 0x00300FF4, 0x00301195, 0x003086B2, 0x003087C1,
            0x0030F78A, 0x003243F9, 0x00324490, 0x00326AA9]
    report("K2b", sites == want, "003105D0 has twelve call sites: %s" % ["%08X" % s for s in sites])
    rs = expect(img, {0x00236A6F: "test byte ptr [rcx], 0x10", 0x00236A75: "je 0x236a7c", 0x00236A77: "call 0x3105d0",
                      0x00236AAC: "mov ebx, 0xffff", 0x00236AFC: "mov word ptr [rdi + 0xdc8], bx"})
    lo, hi = 0x00236A60, 0x00236C24
    e58 = [r for r in disp_sweep(img, 0xE58) if lo <= r[0] < hi]
    report("K2c", not rs and not e58, "00236A60 cancels only when flag-word bit 4 is set (00236A6F/00236A75), writes "
                                      "+0xDC8 = 0xFFFF at 00236AFC either way, and has no +0xE58 access (%d) %s"
           % (len(e58), rs))


# ---------------------------------------------------------------- K3
def k3(img):
    slot0 = img.base + struct.unpack("<I", img.read(0x00305044, 4))[0]
    t = expect(img, {0x0030493C: "movzx eax, byte ptr [rsi + 4]", 0x00304940: "cmp eax, 0xc", 0x00304943: "ja 0x305006",
                     0x00304949: "lea rdx, [rip - 0x1e4950]", 0x00304950: "mov ecx, dword ptr [rdx + rax*4 + 0x1e5044]",
                     0x0030487F: "lea rsi, [rcx + 0x6b0]", 0x00304962: "call 0x30ef20"})
    report("K3a", slot0 == 0x0030495C and not t, "00304850 dispatches on phase byte +0x6B4 (rsi = unit + 0x6B0) through "
                                                 "a 13-slot table at 00305044; slot 0 = %08X runs the prepare at 00304962 %s"
           % (slot0, t))
    zero, regsrc, kinds = [], [], {}
    for site, text, size, acc, fn, st in disp_sweep(img, 0x6B4, width=1):
        if not acc & 2:
            continue
        c = ins(img, site)
        if c.mnemonic == "inc":
            kinds["inc"] = kinds.get("inc", 0) + 1
            continue
        src = c.operands[1]
        if src.type == X86_OP_IMM:
            kinds[src.imm] = kinds.get(src.imm, 0) + 1
            if src.imm == 0:
                zero.append(site)
        else:
            regsrc.append(site)
    # register sources: the commit's sil (xor esi, esi at 0030F796), the cancel's bpl (xor ebp, ebp at 00310649),
    # and 002FE7FB's cl, which is ecx + 1 after `je` on ecx == 0 (002FE7E1-002FE7F2)
    def untouched(reg_names, s, e):
        for c in linear(img, s, e):
            _, w = c.regs_access()
            if any(img.cs.reg_name(r) in reg_names for r in w):
                return False
        return True
    src_ok = (expect(img, {0x0030F796: "xor esi, esi", 0x0030F814: "mov byte ptr [rbx + 0x6b4], sil",
                           0x00310649: "xor ebp, ebp", 0x003106F2: "mov byte ptr [rbx + 0x6b4], bpl",
                           0x002FE7E1: "test ecx, ecx", 0x002FE7E3: "je 0x2fe7f0", 0x002FE7F2: "inc cl",
                           0x002FE7FB: "mov byte ptr [rdx + 0x6b4], cl"}) == []
              and untouched(("rsi", "esi", "si", "sil"), 0x0030F798, 0x0030F814)
              and untouched(("rbp", "ebp", "bp", "bpl"), 0x0031064B, 0x003106F2))
    if src_ok:
        zero += [0x0030F814, 0x003106F2]
    ok = sorted(zero) == [0x0030F814, 0x003106F2] and sorted(regsrc) == [0x002FE7FB, 0x0030F814, 0x003106F2]
    report("K3b", ok, "byte stores of 0 to +0x6B4: %s (immediates %s; register-sourced %s, sources proven %s)"
           % (["%08X" % z for z in sorted(zero)], dict((str(k), v) for k, v in kinds.items()),
              ["%08X" % r for r in sorted(regsrc)], src_ok))
    return ok


# ---------------------------------------------------------------- K4
def k4(img):
    sites = [s for s, f in callers(img, COMMIT)]
    report("K4a", sites == [0x00305B2F, 0x00305C9B, 0x00305DF4, 0x0030FA5C, 0x003130DC],
           "0030F760 call sites: %s" % ["%08X" % s for s in sites])
    arg5 = {}
    for s in sites:
        pd, fn = decode_fn(img, s)
        stores = [fn[a] for a in sorted(fn) if s - 0x48 <= a < s and fn[a].mnemonic == "mov"
                  and fn[a].op_str.startswith("dword ptr [rsp + 0x20], ")]
        arg5[s] = stores[-1].operands[1].imm if stores else None
    report("K4b", arg5 == {0x00305B2F: 1, 0x00305C9B: 1, 0x00305DF4: 1, 0x0030FA5C: 1, 0x003130DC: 0},
           "the 5th argument (cancelFirst) at each site: %s" % dict(("%08X" % k, v) for k, v in arg5.items()))
    c = expect(img, {0x0030F776: "cmp dword ptr [rsp + 0x70], 0", 0x0030F788: "je 0x30f78f",
                     0x0030F78A: "call 0x3105d0"})
    report("K4c", not c, "0030F760 runs the cancel first only when its 5th argument is non-zero %s" % c)
    e = expect(img, {0x00313088: "movzx eax, byte ptr [rbx + 0xea9]", 0x003130A7: "lea rcx, [rax + rax*2]",
                     0x0031309C: "mov dword ptr [rsp + 0x20], 0", 0x003130AB: "movzx eax, word ptr [rbx + 0xdc8]",
                     0x003130B2: "mov word ptr [rdx + rcx*4], ax", 0x003130C1: "mov eax, dword ptr [rbx + 0xe58]",
                     0x003130C7: "mov dword ptr [rdx + rcx*4 + 4], eax", 0x003130D2: "or qword ptr [rbx], 0x400000",
                     0x003130DC: "call 0x30f760", 0x003130E6: "je 0x313109",
                     0x003130F2: "mov byte ptr [rbx + 0x6b4], 5", 0x00313109: "call 0x308270"})
    stash = 0x0031308F + 7 + struct.unpack("<i", img.read(0x0031308F + 3, 4))[0]
    report("K4d", not e and stash == 0x022C1DB0,
           "the engage auto-attack 00312FA0 stashes +0xDC8/+0xE58 at %08X[slot x 12], commits with cancelFirst 0, sets "
           "phase 5 on success and calls the restore on failure %s" % (stash, e))
    r = expect(img, {0x0030827B: "bt rax, 0x16", 0x00308280: "jae 0x3082e2", 0x003082B2: "mov word ptr [rbx + 0xdc8], ax",
                     0x003082C0: "mov dword ptr [rbx + 0xe58], eax"})
    rcalls = sorted(c.operands[0].imm for c in linear(img, 0x00308270, 0x003082E8) if c.mnemonic == "call")
    report("K4e", not r and rcalls == [0x0030C970, 0x0030EDA0],
           "the restore 00308270 (bit 22 only) puts +0xDC8/+0xE58 back and calls only %s - no inventory move %s"
           % (["%08X" % x for x in rcalls], r))
    o = expect(img, {0x00310806: "call 0x308270"})
    pre = [c for c in linear(img, 0x003107A5, 0x00310806) if c.mnemonic.startswith("j")]
    report("K4f", not o and all(j.operands[0].imm <= 0x00310803 for j in pre) and txt(img, 0x00310605) == "call 0x310780",
           "00310780 reaches the restore call 00310806 on every path past its gates, and the cancel calls 00310780 "
           "(00310605) before the refund (0031063A)")


def k4g(img):
    e = expect(img, {0x0030FA20: "call 0x30c010", 0x0030FA54: "mov dword ptr [rsp + 0x20], 1",
                     0x0030FA5C: "call 0x30f760", 0x0030FA63: "je 0x30fa29", 0x0030FA80: "mov byte ptr [rbx + 0x6b4], 5"})
    five = [r[0] for r in disp_sweep(img, 0x6B4, width=1) if r[3] & 2 and len(ins(img, r[0]).operands) == 2
            and ins(img, r[0]).operands[1].type == X86_OP_IMM and ins(img, r[0]).operands[1].imm == 5]
    report("K4g", not e and five == [0x0030FA80, 0x003130F2],
           "the combo continuation 0030FA00 re-commits with cancelFirst 1 and enters phase 5; the phase-5 stores are %s %s"
           % (["%08X" % x for x in five], e))


def k4h(img):
    e = expect(img, {0x0030C3F0: "xor edx, edx", 0x0030C3F9: "mov r8d, 0x180", 0x0030C3FF: "jmp 0x861ec0"})
    tgt = 0x0030C3F2 + 7 + struct.unpack("<i", img.read(0x0030C3F2 + 3, 4))[0]
    report("K4h", not e and tgt == 0x022C1DB0 and callers(img, 0x0030C3F0) == [(0x0023445E, "call")],
           "0030C3F0 memsets %08X for 0x180 bytes (32 x 12) and is called only at 0023445E %s" % (tgt, e))


# ---------------------------------------------------------------- K5
def k5(img):
    e = expect(img, {0x00307300: "push rbp", 0x0030730D: "lea rbp, [rsp - 0xc8]", 0x00307388: "cmp dword ptr [rbp + 0x130], 1",
                     0x0030738F: "jne 0x3073c5", 0x00307398: "call 0x2ffcf0", 0x0030739F: "jne 0x307b91",
                     0x003073AB: "call 0x30ef20", 0x003073B9: "call 0x305640"})
    pushes = [c for c in linear(img, 0x00307300, 0x0030730D) if c.mnemonic == "push"]
    frame = len(pushes) * 8 + 0xC8          # rbp = entry rsp - frame; [rbp + 0x130] = entry rsp + 0x28 = the 5th arg
    sites = callers(img, 0x00307300)
    st = [c for c in linear(img, 0x00319349, 0x00319362) if c.op_str.startswith("dword ptr [rsp + 0x20], ")]
    cr = chain_records(img)
    dr = [d for d in data_refs(img, 0x00307300) if d[2] == "va64" or d[1] not in cr]
    ok = (not e and 0x130 - frame == 0x28 and sites == [(0x00319362, "call")] and len(st) == 1
          and st[0].operands[1].imm == 0 and not dr)
    report("K5", ok, "00307300's prepare+consume arm needs the 5th argument == 1 ([rbp+0x130] = entry rsp + 0x%X); its "
                     "only caller %s stores %s %s" % (0x130 - frame, ["%08X" % s for s, f in sites],
                                                      ["%08X %s" % (c.address, c.op_str) for c in st], e))
    return ok


# ---------------------------------------------------------------- K6, K7, K9, K10
def k6(img):
    e = expect(img, {0x003191FD: "test r14d, r14d", 0x00319200: "jne 0x3192c3",
                     0x00319241: "test byte ptr [rbx + 0x700], 2", 0x0031924F: "jne 0x3192c3",
                     0x003192AE: "mov r8d, 1", 0x003192B7: "call 0x305640", 0x003192BC: "or dword ptr [rbx + 0x700], 2",
                     0x0030F7F2: "and dword ptr [rbx + 0x700], 0xfffffffc",
                     0x003106C5: "and dword ptr [rbx + 0x700], 0xfffffffc"})
    report("K6", not e, "003191B0 consumes once per committed action: first entry, latch +0x700 bit 1 set at 003192BC, "
                        "cleared by the commit 0030F7F2 and the cancel 003106C5 %s" % e)


def k7(img):
    e = expect(img, {0x00304F00: "mov eax, 0xd0", 0x00304F05: "sub r13w, ax", 0x00304F09: "cmp r13w, 0x21",
                     0x00304F0E: "jbe 0x304f3d", 0x00304F22: "test dword ptr [r15 + 0xc], 0x40000000",
                     0x00304F2A: "je 0x304f54", 0x00304F2C: "mov r8d, 1", 0x00304F38: "call 0x305640"})
    report("K7", not e, "00304850's consume runs only for row dword +0x0C bit 30 and id outside 0xD0..0xF1 %s" % e)


def k8(img):
    def discarded(after, stop):
        for c in linear(img, after, stop):
            r, w = c.regs_access()
            rn = [img.cs.reg_name(x) for x in r]
            wn = [img.cs.reg_name(x) for x in w]
            if any(x in ("rax", "eax", "ax", "al") for x in rn):
                return False, "%08X %s %s" % (c.address, c.mnemonic, c.op_str)
            if c.mnemonic == "call" or any(x in ("rax", "eax") for x in wn):
                return True, "%08X %s %s" % (c.address, c.mnemonic, c.op_str)
        return None, "no write"
    a = discarded(0x0030EFB5, 0x0030EFED)
    # refund: the inventory call at 003002CB; on the +0xE58 == 0 path eax survives to the ret, and the cancel overwrites
    # rax at 0031063F before reading it
    b = discarded(0x003002D0, 0x003002E6)          # +0xE58 != 0: the gil call clobbers eax
    b0 = discarded(0x003002FF, 0x0030030A)         # +0xE58 == 0: eax is returned unread ...
    c = discarded(0x0031063F, 0x00310650)          # ... and the cancel overwrites rax before any read
    t = expect(img, {0x003002B6: "cmp cx, di", 0x003002B9: "je 0x3002d7", 0x003002DD: "test edi, edi",
                     0x003002DF: "je 0x3002ff", 0x002FD2E9: "cmp eax, r8d", 0x002FD2EC: "jl 0x2fd30b",
                     0x002FD2F5: "cmp eax, 0x63", 0x002FD2FA: "mov r8d, 0x63", 0x0030EFAA: "or edx, 0xffffffff",
                     0x003002C5: "mov edx, r9d"})
    report("K8t", not t, "the refund's two tests (003002B6, 003002DD), the channel-1 clamp to [equipped, 99] "
                         "(002FD2E9-002FD2FA) and the deltas -1 / +1 read as stated %s" % t)
    report("K8", a[0] is True and b[0] is True and b0[0] is None and c[0] is True,
           "003008A0's return is discarded: prepare %s; refund %s, or returned unread (%s) to the cancel, which writes %s"
           % (a[1], b[1], b0[1], c[1]))


def k9(img):
    e = expect(img, {0x003037C2: "movzx eax, byte ptr [rax + 5]", 0x003037D7: "call 0x3093d0",
                     0x003037EB: "call 0x30b0e0", 0x003037F2: "jne 0x30381c",
                     0x003037F9: "cmp word ptr [rdi + 0xdc8], bx", 0x00303805: "jne 0x30381c",
                     0x0030380C: "mov eax, 0x12", 0x0030B14E: "xor edx, edx", 0x0030B145: "mov rax, qword ptr [rdx + 0x50]",
                     0x0030B158: "setg bl"})
    report("K9", not e, "003037A0 admits when 0030B0E0 (query kind 0 through +0x50, `setg`) is positive or +0xDC8 == "
                        "the item; else 0x12 %s" % e)


def k10(img):
    frags = [(0x00313120, 0x003133F2)]
    calls = sorted(set(c.operands[0].imm for s, e in frags for c in linear(img, s, e)
                       if c.mnemonic == "call" and c.operands[0].type == X86_OP_IMM))
    report("K10b", callers(img, 0x00313120) == [(0x003495B2, "call")], "00313120's only caller is the verb body "
           "003495A0 (003495B2): %s" % ["%08X %s" % c for c in callers(img, 0x00313120)])
    report("K10", CONSUME in calls and PREPARE not in calls and REFUND not in calls and CANCEL not in calls,
           "00313120 (00313120-003133F2) calls the consume and none of prepare / refund / cancel: %s"
           % ["%08X" % x for x in calls])


def k12(img):
    import clos
    seen, ind = clos.closure(0x00304850)
    hit = [x for x in (0x003191B0, 0x00319F50, 0x00325260) if x in seen]
    report("K12", not hit and 0x00305640 in seen and 0x0030EF20 in seen,
           "00304850's direct closure (%d functions, %d indirect call/jmp sites not followed) reaches the reserve and the "
           "consume but not 003191B0 or its callers 00319F50 / 00325260 %s" % (len(seen), ind, ["%08X" % x for x in hit]))


def k13(img):
    """the sites the crossings subsection and the evidence list cite instead of function entries"""
    e = expect(img, {
        0x00308290: "call 0x30c970", 0x003082C6: "call 0x30eda0",                       # the restore's two calls
        0x003056F4: "call 0x300ce0", 0x0030570D: "call 0x300bc0",                       # consume: MP, pool
        0x0030575C: "call 0x316440", 0x003057A5: "call 0x253770", 0x00253770: "jmp 0x316a50",
        0x00254F02: "call 0x316a50",                                                    # setter -> counter update
        0x0030EFCC: "call 0x253690", 0x0030EFD8: "call 0x254ee0",                       # reserve: gil get / set
        0x0030571A: "call 0x253690", 0x0030572B: "call 0x254ee0",                       # consume
        0x003002E1: "call 0x253690", 0x003002F0: "call 0x254ee0",                       # refund
        0x00253697: "mov eax, dword ptr [rax + 8]", 0x00254F09: "mov eax, 0x5f5e0ff",
        0x00254F1F: "mov dword ptr [rax + 8], ecx",
        0x00316449: "movzx ecx, byte ptr [rax + 0x3845]", 0x00316450: "shr ecx, 5", 0x00316458: "mov ecx, 0x13",
        0x0031646D: "jmp 0x8632b0",
        0x0031A022: "call 0x3191b0", 0x00325515: "call 0x3191b0", 0x003495B2: "call 0x313120"})
    g = 0x00253690 + 7 + struct.unpack("<i", img.read(0x00253690 + 3, 4))[0]
    # the category tail: 0 -> (0,1), 1 -> (1,1), 2 -> (2,1), 10 -> 00316440 then (13, id); category 3 reaches neither call
    t = expect(img, {0x00305744: "movzx ecx, byte ptr [r14 + 0x1e]", 0x0030574D: "sub ecx, 1", 0x00305752: "sub ecx, 1",
                     0x00305757: "cmp ecx, 8", 0x0030575A: "jne 0x3057aa"})
    report("K13", not e and not t and g == 0x02092758,
           "crossing and evidence sites read as stated (gil cell %08X; category 3 leaves at 0030575A) %s" % (g, e + t))


# ---------------------------------------------------------------- K11: executed
def k11(img, which="abcdefgh"):
    E = emu
    out = {}

    def fresh():
        return E.World(img)

    if "a" in which:
        W = fresh()
        W.set_owned(3)
        p = W.prepare(E.ROW_ITEM)
        s1 = (W.owned(), W.res(), list(W.idop))
        c = W.consume(E.ROW_ITEM)
        s2 = (W.owned(), W.res(), list(W.idop))
        f = W.refund()
        s3 = (W.owned(), W.res(), list(W.idop))
        out["a"] = report("K11a", p[0] and c[0] and f[0] and s1 == (2, (5, 0), [(5, -1, 0, 1, 0)])
                          and s2 == (2, (0xFFFF, 0), []) and s3 == (2, (0xFFFF, 0), []),
                          "reserve then consume: after prepare %s; after consume %s; a refund after it %s"
                          % (s1, s2, s3))
    if "b" in which:
        W = fresh()
        W.set_owned(3)
        p = W.prepare(E.ROW_ITEM)
        o1 = W.owned()
        f = W.refund()
        s = (W.owned(), W.res(), list(W.idop))
        out["b"] = report("K11b", p[0] and f[0] and o1 == 2 and s == (3, (0xFFFF, 0), [(5, 1, 0, 1, 0)]),
                          "reserve then refund: owned 3 -> %d -> %s" % (o1, s))
    if "c" in which:
        W = fresh()
        W.set_owned(0)
        p = W.prepare(E.ROW_ITEM)
        s1 = (W.owned(), W.res())
        f = W.refund()
        s2 = (W.owned(), W.res())
        out["c"] = (s1, s2)
        report("K11c", p[0] and f[0] and s1 == (0, (5, 0)) and s2 == (1, (0xFFFF, 0)),
               "reserve at owned 0: after prepare %s (nothing taken, reservation set); after refund %s" % (s1, s2))
    if "d" in which:
        W = fresh()
        W.set_owned(99)
        W.w(E.UNIT + 0xDC8, "<H", E.ITEM)
        f = W.refund()
        s = (W.owned(), W.res(), list(W.idop))
        out["d"] = report("K11d", f[0] and s == (99, (0xFFFF, 0), [(5, 1, 0, 1, 0)]),
                          "refund at owned 99: %s - the reserved item is not stored" % (s,))
    if "e" in which:
        W = fresh()
        W.set_owned(3)
        W.prepare(E.ROW_ITEM)
        W.prepare(E.ROW_ITEM)
        s1 = (W.owned(), W.res())
        W.refund()
        s2 = W.owned()
        out["e"] = report("K11e", s1 == (1, (5, 0)) and s2 == 2,
                          "two prepares with no clear between: %s; after one refund owned %d of 3" % (s1, s2))
    if "f" in which:
        W = fresh()
        W.set_owned(3)
        W.w(E.UNIT + 0x698, "<Q", E.KIND1STATS)
        p = W.prepare(E.ROW_ITEM)
        s1 = (W.owned(), W.res(), list(W.idop))
        W.w(E.UNIT + 0xDC8, "<H", E.ITEM)
        f = W.refund()
        s2 = (W.owned(), W.res(), list(W.idop))
        out["f"] = report("K11f", p[0] and f[0] and s1 == (3, (0xFFFF, 0), []) and s2 == (3, (5, 0), []),
                          "kind-1 unit: prepare %s; refund over a planted +0xDC8 %s" % (s1, s2))
    if "g" in which:
        W = fresh()
        W.w(E.STATS + 0x6C, "<B", 1)
        W.prepare(E.ROW_GIL)
        g1 = (W.gil(), W.res())
        W.refund()
        g2 = (W.gil(), W.res())
        W.prepare(E.ROW_GIL)
        W.consume(E.ROW_GIL)
        g3 = (W.gil(), W.res())
        out["g"] = report("K11g", g1 == (610, (0xFFFF, 390)) and g2 == (1000, (0xFFFF, 0)) and g3 == (610, (0xFFFF, 0)),
                          "gil (row +0x0A 31, effect 32): prepare %s; refund %s; prepare + consume %s" % (g1, g2, g3))
    if "h" in which:
        W = fresh()
        res = {}
        for own, eq, rv in ((1, 0, 0xFFFF), (0, 0, 0xFFFF), (0, 0, 5), (0, 0, 6), (1, 1, 0xFFFF), (1, 1, 5)):
            W.set_owned(own, equipped=eq)
            W.w(E.UNIT + 0xDC8, "<H", rv)
            ok, r = W.avail(E.ROW_ITEM)
            res[(own, eq, rv)] = r if ok else "FAULT"
        want = {(1, 0, 0xFFFF): 0, (0, 0, 0xFFFF): 0x12, (0, 0, 5): 0, (0, 0, 6): 0x12, (1, 1, 0xFFFF): 0x12,
                (1, 1, 5): 0}
        out["h"] = report("K11h", res == want, "003037A0 (owned, equipped, +0xDC8) -> reason: %s"
                          % dict(("%d/%d/%X" % k, v) for k, v in res.items()))
    return out


def main():
    print("FABLE check_s29 - S-29 item use: reserve, then consume or refund (2026-10-03)")
    print("unicorn %s" % UC_VERSION)
    img = Img.load()
    print("image sha256 verified (rvlib), base %08X" % img.base)
    report("V0", UC_VERSION == "2.1.4", "unicorn pinned 2.1.4")
    k1(img)
    k2(img)
    k3(img)
    k4(img)
    k4g(img)
    k4h(img)
    k5(img)
    k6(img)
    k7(img)
    k8(img)
    k9(img)
    k10(img)
    k12(img)
    k13(img)
    out = k11(img)

    def failing(fn, im):
        global fails
        quiet[0] = True
        before = fails
        try:
            r = fn(im)
        finally:
            quiet[0] = False
        f = fails - before
        fails = before
        return f > 0, r

    nop7 = b"\x90" * 7
    s1, _ = failing(lambda im: k11(im, "a"), img.patched(0x003056BA, nop7))
    report("S1", s1, "003056BA's 0xFFFF store NOPed: K11a fails, so K11a measures consume's clear")
    s2, _ = failing(lambda im: k11(im, "b"), img.patched(0x0030EFAA, b"\x31\xD2\x90"))
    report("S2", s2, "0030EFAA `or edx, -1` -> `xor edx, edx`: K11b fails, so K11b measures prepare's take")
    s1c, s2c = out["c"]
    claim = (s2c[0] - s1c[0]) <= 0          # what the refund added, against the 0 the prepare took
    report("S3", not claim, "the claim 'a refund never returns more than the prepare took' is refuted by K11c "
                            "(prepare took 0, refund added %d)" % (s2c[0] - s1c[0]))
    s4, _ = failing(k5, img.patched(0x00319354 + 4, b"\x01"))
    report("S4", s4, "00319354 stores 1: K5 fails, so K5 reads the caller's constant")
    s5, _ = failing(k3, img.patched(0x003130F2 + 6, b"\x00"))
    report("S5", s5, "003130F2 stores phase 0: K3 fails, so K3 counts zero writers of +0x6B4")
    print("FAILS %d" % fails)
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
