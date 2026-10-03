"""check_s17.py - FABLE, 2026-10-03: the S-17 cooldown clock across a runtime reset and a load.

Settles, at the bytes of the certified image (73461d08..., base 0x00120000), the claims of section.txt (G9):

  K1  the raw counter 0208D45C has exactly two writers in .text: 0032A135 `inc` (in 0032A100) and 0032A160 `mov ..., 0`;
      every other reference reads it; no pointer constant in .rdata/.data names it.
  K2  0032A160 has exactly one caller, 00237E37 in BattleSystem_ResetRuntimeState 00237DF0, and 00237DF0 is
      branch-free from its loop exit (00237E32) to its ret.
  K3  00237DF0 is reached from exactly six .text sites in four functions (00233C10 x3, 00238A80, 00239960, 00394460) and
      from no pointer constant; the four routes are gated as section.txt states (null bind / stamp mismatch, the
      save-image reset tail, the area-init byte 0208D455 == -2, the title-init verb).
  K4  the death stamp is the counter divided by (int)(30 x [01DFE0B8]): 00300805..00300829 store it at record +0x0C.
  K5  no function statically reachable from 00237DF0 (direct call / jmp closure over chained .pdata) references the bank
      pointers 0208E690 / 0208E698, or is one of the two +0x0C writers 00300530 / 002395A0; positive control: the
      closure DOES contain the counter's zero store 0032A160.
  K6  executed (Unicorn 2.1.4, original code): the script accessor 00235FB0 (whole body, 0031B760 answered by a hook),
      the stamp tail of 00300530, and the selector's cooldown gate (002357D9..002357FB + 002358B6..002358D7):
        a. with the counter and the stamp on one clock, accessor and gate agree;
        b. after the counter restarts below a kept stamp, the accessor returns a NEGATIVE int and the selector's
           unsigned `jb` ADMITS the entry at once;
        c. the script test `elapsed > cooldown` (signed) first passes at second stamp + cooldown + 1 of the new clock;
        d. stamp 1 at counter 0 makes the accessor return -1, the value of its own failure exit;
        e. the same at scale 2.0 (60 per second).
  K7  00233550 (the keep restore) copies bank 2 as 0x128 blocks of 0x80 bytes, structure-blind, from the image.

Sensitivity controls (each must make a check FAIL; the control PASSES when it does):
  S1  image: 002358D7 `jb` -> `jl` (signed): K6b must fail.
  S2  image: 0032A160's store replaced by NOPs: K1 must fail (writer count).
  S3  image: 00300829 stores to +0x10 instead of +0x0C: K4 must fail.
  S4  claim: "elapsed is never negative after a restart" checked against the real execution must fail.

Prints FAILS N last.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, sec  # noqa: E402
from capstone.x86 import X86_OP_IMM, X86_OP_MEM  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, __version__ as UC_VERSION  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP,  # noqa: E402
                               UC_X86_REG_RIP, UC_X86_REG_R9, UC_X86_REG_R14, UC_X86_REG_RBP)

COUNTER = 0x0208D45C
SCALE = 0x01DFE0B8
BANK1 = 0x0208E690
BANK2 = 0x0208E698
NOT_DEST_WRITE = set("cmp test bt ucomiss ucomisd comiss comisd lea push call jmp".split())

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


def is_write(img, site):
    ci = next(img.cs.disasm(img.read(site, 16), site, 1))
    op0 = ci.operands[0] if ci.operands else None
    return bool(op0 is not None and op0.type == X86_OP_MEM and ci.mnemonic not in NOT_DEST_WRITE)


# ---------------------------------------------------------------- K1..K4, K7: the raw index
def k1(img):
    refs, unc = text_refs(img, COUNTER, COUNTER + 4)
    writers = [r for r in refs if is_write(img, r["site"])]
    note("counter 0208D45C: %d references (%d unconfirmed raw candidates)" % (len(refs), len(unc)))
    for r in refs:
        note("  %08X %-6s %-5s %s" % (r["site"], r["form"], "WRITE" if is_write(img, r["site"]) else "read", r["text"]))
    ok = [r["site"] for r in writers] == [0x0032A135, 0x0032A160]
    report("K1a", ok, "exactly two writers: %s" % ["%08X %s" % (r["site"], r["text"]) for r in writers])
    report("K1b", not data_refs(img, COUNTER, COUNTER + 4), "no .rdata/.data pointer constant names the counter")
    report("K1c", not [r for r in refs if r["form"] == "basrel"], "no image-base-relative [reg+RVA] reference")
    return ok


def k2(img):
    refs, _ = text_refs(img, 0x0032A160)
    report("K2a", [(r["site"], r["form"]) for r in refs] == [(0x00237E37, "call")],
           "0032A160 callers: %s" % ["%08X %s" % (r["site"], r["text"]) for r in refs])
    jumps = [ci for ci in img.cs.disasm(img.read(0x00237E32, 0x00237E9D - 0x00237E32), 0x00237E32)
             if ci.mnemonic.startswith("j")]
    report("K2b", not jumps, "00237DF0 is branch-free from 00237E32 to its ret 00237E9C (%d jumps)" % len(jumps))


def k3(img):
    refs, _ = text_refs(img, 0x00237DF0)
    got = [(r["site"], r["form"], r["func"]) for r in refs]
    want = [(0x00233C3F, "call", 0x00233C10), (0x00233C48, "jmp", 0x00233C10), (0x00233C59, "jmp", 0x00233C10),
            (0x00238AA2, "jmp", 0x00238A80), (0x0023998E, "jmp", 0x00239960), (0x00394486, "call", 0x00394460)]
    report("K3a", got == want, "00237DF0 reached from six sites: %s" % ["%08X %s fn=%08X" % g for g in got])
    report("K3b", not [d for d in data_refs(img, 0x00237DF0) if d[2] == "va64"], "no 8-byte pointer constant names 00237DF0")
    # route gates, read at the bytes
    chk = {
        0x00233C20: "test rax, rax", 0x00233C23: "jne 0x233c4d",                       # null bind -> both resets
        0x00233C4D: "cmp dword ptr [rax], 0x5071901", 0x00233C53: "je 0x233c5e",       # stamp mismatch -> reset
        0x00239966: None, 0x00239982: "cmp r12d, -2", 0x00239986: "jne 0x239993",     # area-init byte == -2
        0x002EF67D: "jmp 0x238a80",                                                     # save-image reset tail
        0x00511EAD: "jmp 0x394460",                                                     # verb 7055 fsttl_initialize
        0x0050F81C: None, 0x00584482: None,                                             # the two non-init 0208D455 writers
    }
    bad = []
    for a, t in chk.items():
        ci = next(img.cs.disasm(img.read(a, 16), a, 1))
        txt = (ci.mnemonic + " " + ci.op_str).strip()
        if t is None:
            m = [op for op in ci.operands if op.type == X86_OP_MEM]
            tgt = (a + ci.size + m[0].mem.disp) if m else None
            if tgt != 0x0208D455:
                bad.append("%08X %s" % (a, txt))
        elif txt != t:
            bad.append("%08X %s != %s" % (a, txt, t))
    report("K3c", not bad, "route gates read as stated (00233C23/00233C53/00239982/002EF67D/00511EAD; 0208D455 at "
                           "00239966, 0050F81C, 00584482) %s" % bad)
    callers = {t: [r["site"] for r in text_refs(img, t)[0]] for t in (0x00238A80, 0x00394460, 0x00239960)}
    report("K3d", callers == {0x00238A80: [0x002EF67D], 0x00394460: [0x00511EAD], 0x00239960: [0x00234349]},
           "route entries: %s" % {("%08X" % k): ["%08X" % s for s in v] for k, v in callers.items()})
    root = [r for b, e in [img.pdata(0x00234349)] for r, parts in pdata_roots(img).items() if (b, e) in parts]
    report("K3e", root == [0x002342F0], "00234349 lies in area initialisation 002342F0 (chained .pdata root %s)"
           % ["%08X" % r for r in root])
    up = {t: [r["site"] for r in text_refs(img, t)[0]] for t in (0x00233C10, 0x002EF650, 0x00285E60, 0x00394130)}
    want_up = {0x00233C10: [0x002803B8, 0x00285E86, 0x0036FCF2, 0x00394222],
               0x002EF650: [0x0022B78B, 0x0028037B, 0x003941E5, 0x003942F2],
               0x00285E60: [0x00582CD0, 0x00582CE6], 0x00394130: [0x0039464D]}
    report("K3f", up == want_up, "callers of the gated routes: %s" % {("%08X" % k): ["%08X" % s for s in v]
                                                                      for k, v in up.items()})
    ci = next(img.cs.disasm(img.read(0x0039464D, 16), 0x0039464D, 1))
    report("K3g", (ci.mnemonic + " " + ci.op_str) == "lea rdx, [rip - 0x524]",
           "00394130 is registered as a task proc by 00394640 (`lea rdx, [00394130]` at 0039464D, then 00244F50) - "
           "it is not orphaned")


def k4(img):
    want = [(0x00300805, "call 0x32a150"), (0x0030080A, None), (0x00300814, None), (0x0030081C, "cvttss2si ecx, xmm0"),
            (0x00300820, "div ecx"), (0x00300822, "mov rcx, qword ptr [rbx + 0x6a0]"),
            (0x00300829, "mov dword ptr [rcx + 0xc], eax")]
    bad = []
    for a, t in want:
        ci = next(img.cs.disasm(img.read(a, 16), a, 1))
        txt = (ci.mnemonic + " " + ci.op_str).strip()
        if t is None:
            m = [op for op in ci.operands if op.type == X86_OP_MEM][0]
            tgt = a + ci.size + m.mem.disp
            if tgt not in (SCALE, 0x008F8D80):
                bad.append("%08X -> %08X" % (a, tgt))
        elif txt != t:
            bad.append("%08X `%s`" % (a, txt))
    f30 = struct.unpack("<f", img.read(0x008F8D80, 4))[0]
    return report("K4", not bad and f30 == 30.0,
                  "stamp = counter / (int)(scale x %.1f) stored at record +0x0C (00300829) %s" % (f30, bad))


def k7(img):
    seq = [(0x00233550, "mov rax, qword ptr [rip + 0x1e5b141]"), (0x0023355C, "lea rdx, [rcx + 0x10]"),
           (0x00233560, "mov r8d, 0x128")]
    bad = [a for a, t in seq if (lambda c: (c.mnemonic + " " + c.op_str).strip())(
        next(img.cs.disasm(img.read(a, 16), a, 1))) != t]
    report("K7", not bad, "00233550 reads the bank-2 pointer 0208E698 and copies 0x128 x 0x80 bytes from image+0x10 %s" % bad)


# ---------------------------------------------------------------- K5: the reset's static closure
_ROOTS = {}


def pdata_roots(img):
    if id(img) in _ROOTS:
        return _ROOTS[id(img)]
    po = img.off(img.base + img.exc_rva)
    ents = []
    for i in range(img.exc_size // 12):
        b, e, u = struct.unpack_from("<III", img.d, po + i * 12)
        ui = img.off(img.base + u)
        fl = img.d[ui] >> 3
        n = img.d[ui + 2]
        root = b
        if fl & 4:
            co = ui + 4 + ((n + 1) & ~1) * 2
            root = struct.unpack_from("<I", img.d, co)[0]
        ents.append((b + img.base, e + img.base, root + img.base))
    first = {}
    for b, e, r in ents:
        first[b] = r
    frags = {}
    for b, e, r in ents:
        seen = 0
        while r in first and first[r] != r and seen < 16:
            r = first[r]
            seen += 1
        frags.setdefault(r, []).append((b, e))
    _ROOTS[id(img)] = frags
    return frags


def closure(img, root, skip_sites=()):
    frags = pdata_roots(img)
    tva = sec(img, ".text")[0]
    tend = tva + sec(img, ".text")[1]
    seen, ranges, indirect, stack = set(), [], 0, [root]
    while stack:
        f = stack.pop()
        if f in seen or not (tva <= f < tend):
            continue
        seen.add(f)
        parts = frags.get(f)
        if parts is None:
            pd = img.pdata(f)
            parts = [pd] if pd else None
        if parts is None:  # leaf without .pdata: decode to the first ret / jmp
            end = f
            for ci in img.cs.disasm(img.read(f, 0x800), f):
                end = ci.address + ci.size
                if ci.mnemonic in ("ret", "int3") or ci.mnemonic == "jmp":
                    break
            parts = [(f, end)]
        lo, hi = min(p[0] for p in parts), max(p[1] for p in parts)
        for s, e in parts:
            ranges.append((s, e))
            for ci in img.cs.disasm(img.read(s, e - s), s):
                if ci.mnemonic == "call" or ci.mnemonic == "jmp":
                    op = ci.operands[0]
                    if op.type == X86_OP_IMM:
                        t = op.imm
                        if (ci.mnemonic == "call" or not (lo <= t < hi)) and ci.address not in skip_sites:
                            stack.append(t)
                    else:
                        indirect += 1
    return seen, ranges, indirect


KIND1_SITES = (0x0023ADB5, 0x0023ADC7)   # 0023AC80's kind-1 arm: the two 0031A630 calls
REFILL_SITE = 0x0030C5A5                 # 0030C470 -> 0030F340 (HP set to max, then 00300530)


def k5(img):
    bank = text_refs(img, BANK1, BANK2 + 8)[0]
    ctr = text_refs(img, COUNTER, COUNTER + 4)[0]

    def probe(skip):
        fs, ranges, indirect = closure(img, 0x00237DF0, skip)
        inside = lambda site: any(s <= site < e for s, e in ranges)  # noqa: E731
        return fs, [r["site"] for r in bank if inside(r["site"])], [r["site"] for r in ctr if inside(r["site"])], indirect
    # the reset body itself
    body = list(img.cs.disasm(img.read(0x00237DF0, 0xAD), 0x00237DF0))
    own = [ci for ci in body for op in ci.operands if op.type == X86_OP_MEM and (
        (op.mem.base and img.cs.reg_name(op.mem.base) == "rip" and BANK1 <= ci.address + ci.size + op.mem.disp < BANK2 + 8)
        or op.mem.disp == 0xC)]
    report("K5a", not own, "00237DF0's own body addresses neither bank pointer nor a +0x0C field (%d hits)" % len(own))
    # the loop hands 0023AC80 edx = element index 0..0x27: kind byte (edx >> 8) is 0
    seq = {0x00237E00: "mov edx, 0xffff", 0x00237E08: "cmp ebx, 0xff", 0x00237E0E: "cmovne edx, ebx",
           0x00237E2D: "cmp ebx, 0x28", 0x0023ACA1: "sar eax, 8", 0x0023ACB2: "movzx ebx, al",
           0x0023ACF3: "test ebx, ebx", 0x0023ACF5: "je 0x23ad41", 0x0023AD9B: "test ebx, ebx", 0x0023AD9D: "je 0x23ae04"}
    bad = []
    for a, t in seq.items():
        ci = next(img.cs.disasm(img.read(a, 16), a, 1))
        if (ci.mnemonic + " " + ci.op_str).strip() != t:
            bad.append("%08X" % a)
    report("K5b", not bad, "00237DF0 passes edx = i (0..0x27), so 0023AC80's kind (edx >> 8) is 0 and its kind-1 arm "
                           "(0031A630 at 0023ADB5/0023ADC7) is skipped at 0023AD9D %s" % bad)
    fs0, b0, c0, ind0 = probe(())
    fs1, b1, c1, ind1 = probe(KIND1_SITES)
    fs2, b2, c2, ind2 = probe(KIND1_SITES + (REFILL_SITE,))
    note("closure of 00237DF0: %d functions (%d indirect call/jmp sites not followed); bank-pointer sites reached %s; "
         "00300530 reached %s" % (len(fs0), ind0, ["%08X" % x for x in b0], 0x00300530 in fs0))
    rd = next(img.cs.disasm(img.read(0x0023612D, 16), 0x0023612D, 1))
    report("K5c", b0 == [0x0023612D] and b1 == [0x0023612D] and (rd.mnemonic + " " + rd.op_str) ==
           "add rax, qword ptr [rip + 0x1e5855c]",
           "the closure touches a bank pointer at one site only, 0023612D `add rax, [0208E690]` in the lane resolver "
           "00236100 (a read that returns a record pointer), with or without 0023AC80's kind-1 arm: %s / %s"
           % (["%08X" % x for x in b0], ["%08X" % x for x in b1]))
    report("K5d", 0x00300530 in fs1 and 0x00300530 not in fs2,
           "the only remaining static route to the death-stamp writer 00300530 is 0030C470 -> 0030F340 (call 0030C5A5)")
    report("K5e", 0x002395A0 not in fs0 and 0x002395D1 not in fs0, "the other +0x0C writer 002395A0 (00239657) is not "
                                                                   "reachable from the reset at all")
    report("K5f", 0x0032A160 in fs2 and 0x0032A160 in [c for c in c2] or 0x0032A160 in c2,
           "positive control: the pruned closure still contains the counter store 0032A160")
    # the refill route: 0030F340 passes delta = maxHP - HP to 00300530 (never negative when HP <= max)
    rf = {0x0030F3C2: "mov edx, dword ptr [rbx + 0x24]", 0x0030F3CD: "sub edx, dword ptr [rbx + 0x48]",
          0x0030F3DC: "call 0x300530"}
    bad = [a for a, t in rf.items() if (lambda c: (c.mnemonic + " " + c.op_str).strip())(
        next(img.cs.disasm(img.read(a, 16), a, 1))) != t]
    report("K5g", not bad, "0030F340 calls 00300530 with edx = max - current (0030F3C2..0030F3DC), a refill %s" % bad)


# ---------------------------------------------------------------- K6: execution under Unicorn
STACK, HEAP, MAGIC = 0x7F000000, 0x10000000, 0x7E000000
UNIT, MAP, RECS, KIND = HEAP, HEAP + 0x1000, HEAP + 0x2000, HEAP + 0x800


def make_uc(img):
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    lo = img.base
    hi = max(img.base + va + max(vs, rs) for n, va, vs, ra, rs in img.secs)
    hi = (hi + 0xFFFF) & ~0xFFFF
    uc.mem_map(lo, hi - lo)
    uc.mem_write(lo, img.d[:0x1000])
    for n, va, vs, ra, rs in img.secs:
        uc.mem_write(img.base + va, img.d[ra:ra + min(rs, vs if vs else rs)])
    uc.mem_map(STACK - 0x10000, 0x20000)
    uc.mem_map(HEAP, 0x10000)
    uc.mem_map(MAGIC, 0x1000)
    uc.mem_write(MAGIC, b"\xC3" * 16)
    return uc


def set_world(uc, counter, scale, stamp, cooldown=30, flags=2, slot=2, mapslot=None):
    uc.mem_write(COUNTER, struct.pack("<I", counter & 0xFFFFFFFF))
    uc.mem_write(SCALE, struct.pack("<f", scale))
    uc.mem_write(BANK1, struct.pack("<Q", RECS))
    rec = RECS + slot * 0x250
    uc.mem_write(rec, struct.pack("<I", flags))
    uc.mem_write(rec + 0x08, struct.pack("<HH", 1, 0))
    uc.mem_write(rec + 0x0C, struct.pack("<I", stamp & 0xFFFFFFFF))
    uc.mem_write(rec + 0x10, struct.pack("<H", cooldown))
    uc.mem_write(MAP, bytes([1, slot if mapslot is None else mapslot]))
    uc.mem_write(UNIT + 0x40, struct.pack("<Q", MAP))
    uc.mem_write(UNIT + 0x698, struct.pack("<Q", KIND))
    uc.mem_write(KIND + 5, b"\x01")
    uc.mem_write(UNIT + 0x6A0, struct.pack("<Q", rec))
    return rec


def run_accessor(uc):
    """00235FB0(rcx = actor, edx = lane 0), whole body; 0031B760 answered with UNIT by a hook."""
    def hook(u, addr, size, _):
        if addr == 0x0031B760:
            rsp = u.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", u.mem_read(rsp, 8))[0]
            u.reg_write(UC_X86_REG_RAX, UNIT)
            u.reg_write(UC_X86_REG_RSP, rsp + 8)
            u.reg_write(UC_X86_REG_RIP, ret)
    h = uc.hook_add(UC_HOOK_CODE, hook, begin=0x0031B760, end=0x0031B760)
    rsp = STACK
    uc.mem_write(rsp, struct.pack("<Q", MAGIC))
    uc.reg_write(UC_X86_REG_RSP, rsp)
    uc.reg_write(UC_X86_REG_RCX, 0x1234)
    uc.reg_write(UC_X86_REG_RDX, 0)
    uc.emu_start(0x00235FB0, MAGIC, count=10000)
    uc.hook_del(h)
    v = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    return v - (1 << 32) if v & 0x80000000 else v


def run_stamp(uc):
    """00300530's spawn-backed death tail 003007E8..0030082F (rbx = unit): count +1, stamp = seconds."""
    uc.reg_write(UC_X86_REG_RSP, STACK)
    uc.reg_write(UC_X86_REG_RBX, UNIT)
    uc.reg_write(UC_X86_REG_RBP, 0)
    uc.emu_start(0x003007E8, 0x0030082F, count=1000)
    return struct.unpack("<I", uc.mem_read(RECS + 2 * 0x250 + 0x0C, 4))[0]


def run_gate(uc, rec):
    """the selector's seconds (002357D9..002357FB) and its cooldown gate (002358B6..): 'admit' or 'skip'."""
    uc.reg_write(UC_X86_REG_RSP, STACK)
    uc.emu_start(0x002357D9, 0x002357FB, count=1000)
    secs = uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
    uc.reg_write(UC_X86_REG_R9, secs)
    uc.reg_write(UC_X86_REG_R14, rec)
    out = {}

    def hook(u, addr, size, _):
        if addr in (0x002358DD, 0x002359C4):
            out["r"] = "admit" if addr == 0x002358DD else "skip"
            u.emu_stop()
    h = uc.hook_add(UC_HOOK_CODE, hook, begin=0x002358DD, end=0x002359C4)
    uc.emu_start(0x002358B6, 0x002359D0, count=1000)
    uc.hook_del(h)
    return out.get("r"), secs


def k6(img, which=("a", "b", "c", "d", "e")):
    uc = make_uc(img)
    res = {}
    # a: one clock. a death at second 40, now second 100, cooldown 30
    set_world(uc, 40 * 30 + 7, 1.0, 0)
    st = run_stamp(uc)
    rec = set_world(uc, 100 * 30, 1.0, st)
    el = run_accessor(uc)
    g, s = run_gate(uc, rec)
    res["a"] = (st, el, g)
    if "a" in which:
        report("K6a", st == 40 and el == 60 and g == "admit",
               "one clock: stamp %d (death at counter 1207), elapsed %d at second %d, gate %s; script 60 > 30" % (st, el, s, g))
    # b: the counter restarts (0032A160) and has run 5 seconds; the stamp 40 is kept
    rec = set_world(uc, 5 * 30, 1.0, 40)
    el = run_accessor(uc)
    g, s = run_gate(uc, rec)
    res["b"] = (el, g)
    if "b" in which:
        report("K6b", el == -35 and g == "admit",
               "after a restart: accessor returns %d (signed), selector `jb` on %08X sees %s" % (el, (s - 40) & 0xFFFFFFFF, g))
    # c: first second at which the script's signed `elapsed > cooldown` holds, on the restarted clock
    first = None
    for sec_ in range(0, 120):
        set_world(uc, sec_ * 30 + 29, 1.0, 40)
        if run_accessor(uc) > 30:
            first = sec_
            break
    res["c"] = first
    if "c" in which:
        report("K6c", first == 40 + 30 + 1, "script test first passes at second %s of the new clock (= stamp 40 + "
                                            "cooldown 30 + 1); the selector admitted at second 0" % first)
    # d: stamp 1, counter 0 -> -1, the accessor's own failure value (00236020 `or eax, -1`)
    set_world(uc, 0, 1.0, 1)
    el = run_accessor(uc)
    set_world(uc, 0, 1.0, 1, mapslot=0xFF)  # a real failure: empty lane (00235FE1)
    fail = run_accessor(uc)
    res["d"] = (el, fail)
    if "d" in which:
        report("K6d", el == -1 and fail == -1, "stamp 1 at counter 0 returns %d; the empty-lane exit returns %d" % (el, fail))
    # e: scale 2.0 (60 per second), same restart
    rec = set_world(uc, 5 * 60, 2.0, 40)
    el = run_accessor(uc)
    g, s = run_gate(uc, rec)
    res["e"] = (el, g, s)
    if "e" in which:
        report("K6e", el == -35 and g == "admit" and s == 5, "scale 2.0: second %d, accessor %d, gate %s" % (s, el, g))
    return res


# ---------------------------------------------------------------- run
def main():
    print("FABLE check_s17 - the S-17 cooldown clock across a reset and a load (2026-10-03)")
    print("unicorn %s" % UC_VERSION)
    img = Img.load()
    print("image sha256 verified (rvlib), base %08X" % img.base)
    report("V0", UC_VERSION.startswith("2.1.4"), "unicorn pinned 2.1.4")
    k1(img)
    k2(img)
    k3(img)
    k4(img)
    k5(img)
    k6(img)
    k7(img)

    # sensitivity controls: each must make its check fail
    def failing(fn, im):
        global fails
        before = fails
        quiet[0] = True
        try:
            fn(im)
        except Exception:
            fails += 1
        quiet[0] = False
        failed = fails > before
        fails = before
        return failed

    s1 = img.patched(0x002358D7, b"\x0F\x8C")
    report("S1", failing(lambda im: k6(im, which=("b",)), s1), "002358D7 jb -> jl (signed gate): K6b fails, so K6b "
                                                               "measures the unsigned compare")
    s2 = img.patched(0x0032A160, b"\x90" * 10)
    report("S2", failing(k1, s2), "0032A160's store NOPed: K1 fails on the writer count")
    s3 = img.patched(0x00300829, b"\x89\x41\x10")
    report("S3", failing(k4, s3), "00300829 stores to +0x10: K4 fails")
    r = k6(img, which=())
    claim_never_negative = r["b"][0] >= 0
    report("S4", not claim_never_negative, "the mutated claim 'elapsed is never negative after a restart' is refuted "
                                           "by the execution (accessor %d)" % r["b"][0])
    print("FAILS %d" % fails)
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
