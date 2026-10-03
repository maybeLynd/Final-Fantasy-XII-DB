"""check_sd199b.py - FABLE, 2026-10-03.  The static remainder of SD-199, settled at the bytes.

Question 1: what the "per-vertex compare" at 0039A0C6 (in 00399B80) and 0039A6C8 (in 0039A150) tests.
Question 2: whether 0039A150 ever writes a vertex entry whose first qword is zero (the only trigger of the
            zero-corner drop in 00437130 / 00444340), into the buffer those drawers read.

Register names follow the bank page (00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md):
GPR[k] = 022D8F10 + 16k, so $zero = 022D8F10, v0 = 022D8F30, t0..t5 = 022D8F90..022D8FE0, t7 = 022D9000;
vector rows 1..4 = 022D91B0..022D91EF; vf00.w = [01EF93FC] = 1.0.

Sections
  S   structure of both bodies: decode, extent, loop, strides, the clamp, the compare, every store (static anchors)
  Z   $zero (022D8F10) has no writer image-wide (aligned raw sweep), lies in .data's zero-filled tail, and every
      pointer to it is passed as a source
  B   buffer identity: the entries 0039A150 writes are the corners 00437130 / 00444340 test
  E   execution under Unicorn of the original bytes of both functions: fixed edge vertices and 2,000 random ones
      against a float32 model of the reading in S
  C   controls (must be sensitive to the defect they name)

Run: python check_sd199b.py > check_sd199b.out   (exit 1 when any check fails)
"""
import os
import random
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RV = os.path.join(HERE, "..", "fable-review-astra-ov42-caller-quotient-bound-1002")
sys.path.insert(0, RV)
from rvlib import Img, Report, Body, expect  # noqa: E402
from capstone.x86 import X86_OP_MEM  # noqa: E402
import numpy as np  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RSP, UC_X86_REG_R8,  # noqa: E402
                               UC_X86_REG_R9, UC_X86_REG_RAX)

T0S, T0E = 0x399B80, 0x39A14A      # 00399B80, bit 3 clear
T1S, T1E = 0x39A150, 0x39A766      # 0039A150, bit 3 set
ZERO = 0x22D8F10                   # GPR[0] $zero
V0, T1R, T2R, T3R, T4R, T5R, T7R = 0x22D8F30, 0x22D8FA0, 0x22D8FB0, 0x22D8FC0, 0x22D8FD0, 0x22D8FE0, 0x22D9000
ROWS = 0x22D91B0
f32 = np.float32


def rip_t(I):
    """Resolved rip-relative target of an Insn (or None)."""
    for m in I.mems:
        if m["base"] == "rip":
            return I.address + I.size + m["disp"]
    return None


def at(R, B, a, mnem, ops=None, target=None, name=None):
    I = B.ins.get(a)
    ok = I is not None and I.mnemonic == mnem and (ops is None or I.op_str == ops) and (
        target is None or rip_t(I) == target)
    got = "<no boundary>" if I is None else "%s %s%s" % (I.mnemonic, I.op_str,
                                                      (" ->%08X" % rip_t(I)) if rip_t(I) else "")
    want = "%s %s%s" % (mnem, ops or "", (" ->%08X" % target) if target else "")
    return R.check(name or "%08X is `%s`" % (a, want.strip()), ok, "" if ok else "got `%s`" % got)


def stores(B, home_base=None, home_end=0):
    """Every memory write split into (pointer stores, other).  Excluded from 'pointer stores': rip-relative globals,
    rsp frame slots, bank globals addressed as [rsi + rax + 0x21B8xxx] with rsi = the image base (checked by the
    caller), and the prologue's home/xmm saves through `home_base` before `home_end`."""
    ptr, other = [], []
    for a in B.order:
        I = B[a]
        for m in I.mems:
            if not m["write"] or I.mnemonic in ("lea", "nop"):
                continue
            row = (a, I.mnemonic, I.op_str, m["size"])
            if m["base"] in ("rip", "rsp"):
                other.append(row)
            elif "rsi" in (m["base"], m["index"]) and 0x21B8F00 <= (m["disp"] & 0xFFFFFFFF) < 0x21BA000:
                other.append(row)
            elif m["base"] == home_base and a < home_end:
                other.append(row)
            else:
                ptr.append(row)
    return ptr, other


def no_write_between(B, lo, hi, reg, allow_branch=()):
    """No instruction in (lo, hi) writes `reg` (family); none is a branch (other than `allow_branch`, whose
    fall-through continues the range) and none is the target of a branch."""
    tg = set()
    for a in B.order:
        t = B[a].direct_target()
        if t is not None and B[a].mnemonic.startswith("j"):
            tg.add(t)
    for a in B.order:
        if lo < a < hi:
            I = B[a]
            if reg in I.reg_writes or (I.mnemonic.startswith("j") and a not in allow_branch) or a in tg:
                return False, "%08X %s" % (a, I.text)
    return True, ""


# ============================================================================================== S
def section_s(img, R):
    print("== S: structure of 00399B80 and 0039A150")
    B0, B1 = Body(img, T0S, T0E), Body(img, T1S, T1E)
    R.check("S0 00399B80 decodes exactly over 1,482 bytes and is one .pdata function (00399B80..0039A14A)",
            B0.exact and img.pdata(T0S) == (T0S, T0E))
    R.check("S0 0039A150 decodes exactly over 1,558 bytes and is one .pdata function (0039A150..0039A766)",
            B1.exact and img.pdata(T1S) == (T1S, T1E))
    for B, nm in ((B0, "00399B80"), (B1, "0039A150")):
        calls = [a for a in B.order if B[a].mnemonic == "call"]
        rets = [a for a in B.order if B[a].mnemonic == "ret"]
        R.check("S0 %s is call-free with one ret" % nm, not calls and len(rets) == 1)
    R.check("S0 constants: [01CEBC84] = 16.0f (the X,Y scale), [01EF93FC] = 1.0f (vf00.w)",
            img.read(0x1CEBC84, 4) == struct.pack("<f", 16.0) and img.read(0x1EF93FC, 4) == struct.pack("<f", 1.0))

    R.note("-- 00399B80 (bit 3 clear): inputs rcx = float4 vertices (stride 16), rdx = entries (stride 16), "
           "r8 = float Q out (stride 4), r9d = count")
    for a, m, o, t in [
            (0x399B9C, "movups", "xmm0, xmmword ptr [rcx]", None),          # vertex 0 -> vf (022D9300)
            (0x399C60, "movss", None, 0x22D9304),                          # loop head: reads vertex.y
            (0x399C68, "add", "edi, 0x10", None),                          # input stride 16 (low dword of [rsp+0x50])
            (0x399DA3, "divss", "xmm1, xmm0", None),                       # Q = 1.0 / W
            (0x399DCB, "mulss", "xmm7, xmm8", None),                       # X *= 16
            (0x399DFB, "cvttss2si", "eax, xmm7", None),
            (0x399E09, "cvttss2si", "eax, xmm6", None),
            (0x399E17, "cvttss2si", "eax, xmm3", None),
            (0x399EAD, "movd", "dword ptr [rbx], xmm2", None),            # Q store
            (0x399EB1, "add", "rbx, 4", None),
            (0x399ECE, "cmp", "edx, ecx", None), (0x399ED0, "jle", "0x399edb", None),     # PMAXW t1 = max(t0, t4)
            (0x399EF7, "cmp", None, None), (0x399EFE, "jl", "0x399f07", None),            # PMINW t1 = min(t1, t2)
            (0x399F1A, "movups", None, ZERO),                               # xmm4 = $zero
            (0x399FA0, "cmp", None, 0x22D8F90), (0x399FAE, "setne", "cl", None), (0x399FB6, "dec", "ecx", None),
            (0x39A04A, "mov", None, 0x22D8F90), (0x39A051, "or", None, T5R), (0x39A087, "inc", "rcx", None),
            (0x39A0AC, "movq", "rax, xmm4", None),
            (0x39A0C6, "cmp", "rcx, rax", None), (0x39A0C9, "jne", "0x39a122", None),
            (0x39A0CB, "mov", None, T7R), (0x39A0D6, "mov", None, T1R), (0x39A0DD, "or", None, T3R),
            (0x39A0E4, "or", "rcx, rax", None), (0x39A0F6, "mov", "qword ptr [r11], rcx", None),
            (0x39A0D2, "add", "r8d, 0x10", None),
            (0x39A0EC, "movsxd", "rax, r9d", None), (0x39A0F9, "mov", None, ZERO),
            (0x39A107, "cmp", "rax, r10", None), (0x39A10A, "je", "0x39a116", None),
            (0x39A111, "jmp", "0x399c60", None),
            (0x39A116, "mov", None, V0), (0x39A11D, "mov", "eax, r10d", None),
            (0x39A122, "mov", None, V0)]:
        at(R, B0, a, m, o, t)
    R.check("S1 rsi is the image base in both bodies (`lea rsi` -> 00120000 at 00399BA6 and 0039A16F), so "
            "[rsi + rax + 0x21B8Fxx] are bank registers (022D8Fxx)",
            rip_t(B0[0x399BA6]) == img.base and rip_t(B1[0x39A16F]) == img.base and
            not [a for a in B0.order if a != 0x399BA6 and "rsi" in B0[a].reg_writes and B0[a].mnemonic != "pop"] and
            not [a for a in B1.order if a != 0x39A16F and "rsi" in B1[a].reg_writes and B1[a].mnemonic not in ("pop", "push")])
    s0, o0 = stores(B0)
    R.check("S1 00399B80's only stores through a pointer are the entry qword `mov qword ptr [r11], rcx` "
            "(0039A0F6) and the Q dword (00399EAD); everything else goes to the bank or the frame (%d)" % len(o0),
            [(a, w) for a, _, _, w in s0] == [(0x399EAD, 4), (0x39A0F6, 8)], str(s0))
    R.check("S1 00399B80 decrements the count once per vertex (`dec r9d` 00399E3B) and the vertex loop's only back "
            "edge is 0039A111 -> 00399C60",
            B0[0x399E3B].text == "dec r9d" and
            [a for a in B0.order if B0[a].mnemonic.startswith("j") and (B0[a].direct_target() or 1 << 40) < a
             and B0[a].direct_target() <= 0x399C60] == [0x39A111])

    R.note("-- 0039A150 (bit 3 set): same inputs; rcx/rdx are advanced through their home slots [rsp+0x70]/[rsp+0x78]")
    for a, m, o, t in [
            (0x39A184, "mov", "r11, rdx", None), (0x39A1AA, "mov", "r10d, edx", None),
            (0x39A1C9, "add", "edi, 0x10", None), (0x39A1E4, "movups", "xmm6, xmmword ptr [rax]", None),
            (0x39A1EA, "mov", None, T3R), (0x39A34B, "divss", "xmm3, xmm0", None),
            (0x39A3C3, "mov", None, T3R), (0x39A3CE, "mov", None, T5R),
            (0x39A3E1, "mov", None, V0), (0x39A3A9, "or", "r8, 1", None),
            (0x39A4A7, "movd", "dword ptr [rbx], xmm2", None),
            (0x39A4CE, "cmp", "edx, ecx", None), (0x39A4D0, "jle", "0x39a4db", None),
            (0x39A4FE, "jl", "0x39a507", None),
            (0x39A51A, "movups", None, ZERO),
            (0x39A680, "mov", None, 0x22D8F90), (0x39A687, "or", None, T5R), (0x39A68E, "inc", "rax", None),
            (0x39A6A5, "add", "r10d, 0x10", None), (0x39A6B1, "movq", "rcx, xmm4", None),
            (0x39A6C8, "cmp", "rax, rcx", None), (0x39A6CB, "je", "0x39a6f0", None),
            (0x39A6CD, "mov", "qword ptr [r11], rcx", None),
            (0x39A6F0, "mov", None, T2R), (0x39A6F7, "mov", None, T1R), (0x39A6FE, "or", None, T3R),
            (0x39A705, "or", "rcx, rax", None), (0x39A712, "mov", "qword ptr [r11], rcx", None),
            (0x39A6EB, "jmp", "0x39a1c0", None), (0x39A72D, "jmp", "0x39a1c0", None),
            (0x39A732, "mov", None, V0)]:
        at(R, B1, a, m, o, t)
    R.check("S2 constants: rbp = 0xFF00000000000000 (0039A18C) and r14 = 0xFFFF000000000000 (0039A19B); "
            "[t3] = 0xFFFFFF at 0039A1EA",
            B1[0x39A18C].text == "movabs rbp, 0xff00000000000000" and
            B1[0x39A19B].text == "movabs r14, 0xffff000000000000" and
            B1[0x39A1EA].text.endswith(", 0xffffff") and B1[0x39A3C3].text.endswith(", rbp") and
            B1[0x39A3CE].text.endswith(", r14"))
    s1, o1 = stores(B1, home_base="rax", home_end=0x39A1A5)
    R.check("S2 0039A150's only stores through a pointer are two entry qwords `mov qword ptr [r11], rcx` "
            "(0039A6CD unequal arm, 0039A712 equal arm) and the Q dword (0039A4A7); everything else goes to the bank, "
            "the frame or the prologue's home slots (%d)" % len(o1),
            [(a, w) for a, _, _, w in s1] == [(0x39A4A7, 4), (0x39A6CD, 8), (0x39A712, 8)], str(s1))
    ok, why = no_write_between(B1, 0x39A51A, 0x39A6B1, "xmm4")
    ok2, why2 = no_write_between(B1, 0x39A6B1, 0x39A6CD, "rcx", allow_branch=(0x39A6CB,))
    R.check("S3 the unequal arm stores $zero's low qword: xmm4 <- [022D8F10] at 0039A51A, rcx <- xmm4 at 0039A6B1, "
            "store at 0039A6CD; straight-line code with no write to xmm4 / rcx and no branch or branch target between",
            ok and ok2, why + why2)
    t3w = [a for a in B1.order for m in B1[a].mems if m["write"] and m["base"] == "rip" and
           B1[a].address + B1[a].size + m["disp"] < T3R + 8 and B1[a].address + B1[a].size + m["disp"] + m["size"] > T3R]
    R.check("S3 the equal arm ORs t3, whose only writers are 0039A1EA (0xFFFFFF, loop top, consumed by the t2 bound "
            "build) and 0039A3C3 (0xFF00000000000000, after it): the stored qword's top byte is 0xFF, never 0",
            t3w == [0x39A1EA, 0x39A3C3], str(["%08X" % a for a in t3w]))
    R.check("S3 0039A150 returns v0 = $zero | 1 (`or r8, 1` 0039A3A9, `mov [v0], r8` 0039A3E1, `mov eax, [v0]` "
            "0039A732) whatever the compares gave; its callers ignore it",
            B1[0x39A3A9].text == "or r8, 1")
    R.check("S4 the loop test is a separate compare in both bodies: `movsxd rax, r9d` against $zero "
            "(00399B80: 0039A107 `cmp rax, r10`, r10 <- [022D8F10] at 0039A0F9; 0039A150: 0039A6E1 / 0039A723 "
            "`cmp rax, r8`, r8 <- [022D8F10] at 0039A6D0 / 0039A715)",
            B1[0x39A6E1].text == "cmp rax, r8" and B1[0x39A723].text == "cmp rax, r8" and
            rip_t(B1[0x39A6D0]) == ZERO and rip_t(B1[0x39A715]) == ZERO)
    return B0, B1


# ============================================================================================== Z
def exec_sections(img):
    pe = struct.unpack_from("<I", img.d, 0x3C)[0]
    nsec = struct.unpack_from("<H", img.d, pe + 6)[0]
    optsz = struct.unpack_from("<H", img.d, pe + 20)[0]
    off = pe + 24 + optsz
    out = []
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", img.d, off + 8)
        ch = struct.unpack_from("<I", img.d, off + 36)[0]
        if ch & 0x20000000:
            out.append((va, rs, ra))
        off += 40
    return out


def zero_writers(img, lo=ZERO, hi=ZERO + 16):
    """Raw byte sweep for any disp32 that can resolve into [lo, hi) (rip-relative with 0/1/2/4 immediate bytes,
    absolute, or image-base-relative), confirmed at instruction boundaries of the .pdata function holding it
    (or a resync decode when there is none).  Returns (writes, reads, leas)."""
    rel_lo, rel_hi = lo - img.base, hi - img.base
    cand = set()
    for va, rs, ra in exec_sections(img):
        blob = img.d[ra:ra + rs]
        base = img.base + va
        for i in range(len(blob) - 4):
            d = struct.unpack_from("<i", blob, i)[0]
            u = d & 0xFFFFFFFF
            s = base + i
            if lo - 4 - 16 < s + d < hi or lo <= u < hi or rel_lo <= u < rel_hi:
                cand.add(s)
    by_fn, loose = {}, []
    for s in cand:
        p = img.pdata(s)
        if p:
            by_fn.setdefault(p, []).append(s)
        else:
            loose.append(s)
    insns = []
    for (fs, fe), sites in by_fn.items():
        for ci in img.cs.disasm(img.read(fs, fe - fs), fs):
            if any(ci.address < x < ci.address + ci.size for x in sites):
                insns.append(ci)
    for x in loose:
        for back in range(1, 12):
            ci = next(img.cs.disasm(img.read(x - back, 24), x - back), None)
            if ci and ci.address < x < ci.address + ci.size:
                # accept only if a 48-byte-earlier decode re-synchronises on this instruction
                for pre in range(16, 64):
                    seq = list(img.cs.disasm(img.read(ci.address - pre, pre + ci.size), ci.address - pre))
                    if any(c.address == ci.address for c in seq):
                        insns.append(ci)
                        break
                break
    writes, reads, leas = [], [], []
    seen = set()
    for ci in insns:
        if ci.address in seen:
            continue
        seen.add(ci.address)
        for k, op in enumerate(ci.operands):
            if op.type != X86_OP_MEM:
                continue
            m = op.mem
            bn = ci.reg_name(m.base) if m.base else None
            if bn == "rip":
                t = ci.address + ci.size + m.disp
            else:
                dd = m.disp & 0xFFFFFFFF
                t = dd + (img.base if rel_lo <= dd < rel_hi else 0)
            if not (t < hi and t + max(op.size, 1) > lo):
                continue
            row = (ci.address, ci.mnemonic, ci.op_str, bn, op.size)
            if ci.mnemonic == "lea":
                leas.append(row)
            elif k == 0 and ci.mnemonic not in ("cmp", "test", "push", "call", "jmp", "ucomiss", "comiss", "bt"):
                writes.append(row)
            else:
                reads.append(row)
    return sorted(writes), sorted(reads), sorted(leas)


def section_z(img, R):
    print("== Z: $zero (022D8F10) is zero")
    w, r, l = zero_writers(img)
    R.check("Z1 image-wide raw sweep (rip-relative, absolute and image-base-relative disp32 into 022D8F10..1F, "
            "confirmed at instruction boundaries): 0 writers", not w, str(w[:4]))
    R.note("   readers %d, address-takers (lea) %d" % (len(r), len(l)))
    R.check("Z1 the sweep is live: it reports the reads this record relies on (0039A51A, 0039A0F9) among its "
            "read sites",
            len(r) > 2 and 0x39A51A in [x[0] for x in r] and 0x39A0F9 in [x[0] for x in r], "%d reads" % len(r))
    # every lea of 022D8F10 is passed as rdx to 003CCA70, which writes only through rcx
    bad = []
    for a, mn, ops, bn, sz in l:
        if not ops.startswith("rdx,"):
            bad.append("%08X %s" % (a, ops))
            continue
        p = img.pdata(a)
        seq = list(img.cs.disasm(img.read(a, 0x200), a))
        call = next((c for c in seq if c.mnemonic == "call"), None)
        rdx_clob = any(c.op_str.startswith("rdx,") or c.op_str.startswith("edx,") for c in seq[1:seq.index(call)]) \
            if call else True
        if call is None or call.op_str != "0x3cca70" or rdx_clob:
            bad.append("%08X -> %s" % (a, call.op_str if call else None))
    cc = list(img.cs.disasm(img.read(0x3CCA70, 0x200), 0x3CCA70))
    end = next(i for i, c in enumerate(cc) if c.mnemonic == "ret")
    cc = cc[:end + 1]
    dst = set()
    for c in cc:
        for k, op in enumerate(c.operands):
            if op.type == X86_OP_MEM and k == 0 and c.mnemonic not in ("cmp", "test"):
                dst.add(c.reg_name(op.mem.base))
    no_rcx_write = not any(c.op_str.split(",")[0] in ("rcx", "ecx") for c in cc)
    R.check("Z2 all %d address-takers of 022D8F10 load it into rdx for the next call, 003CCA70, and 003CCA70 "
            "(%d instructions to its ret) stores only through rcx, which it never modifies" % (len(l), len(cc)),
            l and not bad and dst == {"rcx"} and no_rcx_write, "bad %s dst %s" % (bad, dst))
    data = [s for s in img.secs if s[0] == ".data"][0]
    name, va, vs, ra, rs = data
    tail = img.base + va + rs
    R.check("Z3 022D8F10 lies in .data's zero-filled tail (raw data ends at %08X, virtual end %08X): "
            "zero at load" % (tail, img.base + va + vs), tail <= ZERO < img.base + va + vs)
    R.note("   not covered by Z1: a store through a computed pointer whose base is not 022D8F10.  The nearest such "
           "family is the heap counter array 022D8E10 (`sub/add [base + id*4]`, 0036C60C, 0036D0FE), which "
           "reaches 022D8F10 only at index 64, while a separately addressed global sits at 022D8E50 (index 16)")
    return w


# ============================================================================================== B
def section_b(img, R):
    print("== B: the entries 0039A150 writes are the corners the drawers test")
    D = Body(img, 0x4355D0, 0x4355D0 + 5936)
    before = R.fails
    P5 = Body(img, 0x435050, 0x4352B2)
    P4 = Body(img, 0x434CD0, 0x435050)
    F = Body(img, 0x437130, 0x437130 + 5930)
    for B, a, m, o, t in [
            (P5, 0x435073, "movzx", "edi, word ptr [rcx + 0x16]", None), (P5, 0x435082, "mov", None, 0x2AEED50),
            (P5, 0x435090, "shl", "rdi, 5", None), (P5, 0x435097, "add", "rdi, r12", None),
            (P5, 0x43511F, "mov", "rdx, rdi", None), (P5, 0x435122, "call", "0x39a150", None),
            (P4, 0x434CF1, "movzx", "esi, word ptr [rcx + 0x16]", None), (P4, 0x434D32, "mov", None, 0x2AEED50),
            (P4, 0x434D57, "shl", "rsi, 5", None), (P4, 0x434D5B, "add", "rsi, rax", None),
            (P4, 0x434E01, "mov", "rdx, rsi", None), (P4, 0x434E04, "mov", "rcx, rsi", None),
            (P4, 0x434E0D, "call", "0x39a150", None),
            (F, 0x437160, "mov", None, 0x2AEED50), (F, 0x437175, "movzx", "eax, word ptr [rsi + 0x16]", None),
            (F, 0x43717E, "shl", "rax, 4", None), (F, 0x437182, "add", "rcx, rax", None),
            (F, 0x437191, "lea", "r14, [rax + rcx]", None),
            (F, 0x43785F, "add", "rcx, rcx", None), (F, 0x437862, "movaps", "xmm0, xmmword ptr [r14 + rcx*8]", None),
            (F, 0x43786D, "movdqa", "xmmword ptr [rbp + 0x60], xmm0", None),
            (F, 0x43789C, "cmp", "qword ptr [rbp + 0x60], 0", None),
            (D, 0x4355FC, "mov", "rsi, rcx", None), (D, 0x435633, "mov", "rcx, rsi", None),
            (D, 0x435663, "mov", "rcx, rsi", None), (D, 0x43568F, "mov", "rcx, rsi", None),
            (D, 0x435692, "call", "0x437130", None)]:
        at(R, B, a, m, o, t)
    R.check("B1 mesh: both preps write entries at [02AEED50] + 32*word[+0x16] (16-byte stride), and 00437130 reads "
            "corner idx at [02AEED50] + 16*w + 16*w + 16*idx = the same base and stride, for the same element "
            "(004355D0 passes rsi to the prep and to 00437130): all %d anchors above" % 27, R.fails == before)
    path = D.reach(0x4355FF, avoid=[0x435641, 0x435699])
    rsi_w = [a for a in path if "rsi" in D[a].reg_writes]
    R.check("B1 on every path from 004355FF to the 00437130 call (not through the shared epilogue 00435641 or the "
            "inline path 00435699) nothing writes rsi; the path reaches 00435692",
            not rsi_w and 0x435692 in path, str(["%08X" % a for a in rsi_w]))
    G1 = Body(img, 0x444340, 0x444340 + 3979)
    for B, a, m, o, t in [(G1, 0x444366, "mov", None, 0x2AEED58), (G1, 0x444377, "mov", "qword ptr [rsp + 0x58], rbx", None),
                          (G1, 0x444B5B, "mov", "r15, qword ptr [rsp + 0x58]", None),
                          (G1, 0x444B82, "add", "rsi, r15", None), (G1, 0x444B90, "movaps", "xmm2, xmmword ptr [rsi]", None),
                          (G1, 0x444BD5, "test", "rax, rax", None)]:
        at(R, B, a, m, o, t)
    ok = True
    det = []
    for w, n, c1 in ((0x4453D0, 1914, 0x44578A), (0x447020, 2062, 0x447463), (0x447ED0, 2350, 0x448426)):
        Bw = Body(img, w, w + n)
        k = Bw.order.index(c1)
        prev = [Bw[a] for a in Bw.order[max(0, k - 30):k]]
        src = [I for I in prev if I.mnemonic == "mov" and I.op_str.startswith("rcx, qword ptr [rip") and rip_t(I) == 0x2AEED58]
        cp = [I for I in prev if I.text == "mov rdx, rcx"]
        good = Bw[c1].text == "call 0x39a150" and bool(src) and bool(cp) and src[-1].address < cp[-1].address
        ok &= good
        det.append("%08X:%s" % (c1, good))
    R.check("B2 grid: each walk calls 0039A150 in place on rcx = rdx = [02AEED58], and 00444340 reads its corners "
            "from [02AEED58] (+16*index); anchors above", ok, " ".join(det))
    wr = []
    for va, rs, ra in exec_sections(img):
        blob = img.d[ra:ra + rs]
        base = img.base + va
        for i in range(len(blob) - 4):
            d = struct.unpack_from("<i", blob, i)[0]
            if base + i + 4 + d == 0x2AEED58 or base + i + 4 + d == 0x2AEED50:
                p = img.pdata(base + i)
                if not p:
                    continue
                for ci in img.cs.disasm(img.read(p[0], p[1] - p[0]), p[0]):
                    if ci.address < base + i < ci.address + ci.size:
                        I = Body(img, ci.address, ci.address + ci.size)[ci.address]
                        if any(m["write"] and m["base"] == "rip" for m in I.mems):
                            wr.append((ci.address, rip_t(I)))
    wr = sorted(set(wr))
    R.check("B3 the scratch pointers' only writers: 02AEED50 at 0039CD6B; 02AEED58 at 00434D62 (prep 00434CD0) and "
            "at 004454FD / 004471BF / 00448073 (the three walks, before their transform call); none in "
            "00437130 or 00444340",
            wr == [(0x39CD6B, 0x2AEED50), (0x434D62, 0x2AEED58), (0x4454FD, 0x2AEED58), (0x4471BF, 0x2AEED58),
                   (0x448073, 0x2AEED58)], str([("%08X" % a, "%08X" % t) for a, t in wr]))


# ============================================================================================== E
class Bench(object):
    VERT, OUT, QOUT, STK, RET = 0x10000000, 0x10010000, 0x10020000, 0x20000000, 0x30000000

    def __init__(self, img):
        self.mu = mu = Uc(UC_ARCH_X86, UC_MODE_64)
        pe = struct.unpack_from("<I", img.d, 0x3C)[0]
        size = (struct.unpack_from("<I", img.d, pe + 24 + 56)[0] + 0xFFF) & ~0xFFF
        mu.mem_map(img.base, size)
        for name, va, vs, ra, rs in img.secs:
            mu.mem_write(img.base + va, img.d[ra:ra + min(rs, vs if vs else rs)])
        mu.mem_map(0x10000000, 0x30000)
        mu.mem_map(self.STK, 0x10000)
        mu.mem_map(self.RET, 0x1000)
        mu.mem_write(self.RET, b"\xf4")

    def set_matrix(self, M):
        self.mu.mem_write(ROWS, b"".join(struct.pack("<4f", *r) for r in M))

    def run(self, fn, verts):
        mu = self.mu
        n = len(verts)
        mu.mem_write(self.VERT, b"".join(struct.pack("<4f", x, y, z, 1.0) for x, y, z in verts) + b"\0" * 16)
        mu.mem_write(self.OUT, b"\xA5" * (16 * n))
        mu.mem_write(self.QOUT, b"\x5A" * (4 * n))
        rsp = self.STK + 0xF000
        mu.mem_write(rsp, struct.pack("<Q", self.RET) + b"\0" * 0x60)
        mu.reg_write(UC_X86_REG_RSP, rsp)
        mu.reg_write(UC_X86_REG_RCX, self.VERT)
        mu.reg_write(UC_X86_REG_RDX, self.OUT)
        mu.reg_write(UC_X86_REG_R8, self.QOUT)
        mu.reg_write(UC_X86_REG_R9, n)
        mu.emu_start(fn, self.RET, count=200000 * max(1, n))
        eax = mu.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF
        out = bytes(mu.mem_read(self.OUT, 16 * n))
        q = bytes(mu.mem_read(self.QOUT, 4 * n))
        return eax, [out[16 * k:16 * k + 8] for k in range(n)], [out[16 * k + 8:16 * k + 16] for k in range(n)], \
            [q[4 * k:4 * k + 4] for k in range(n)]


def cvtt(v):
    v = float(v)
    if v != v or v >= 2147483648.0 or v < -2147483648.0:
        return -2147483648
    return int(v)


BOUNDS = ((0, 0xFFF0), (0, 0xFFF0), (0xFF, 0xFFFFFF))


def model(M, v, bounds=BOUNDS):
    """float32 model of the reading in S: (in_range, entry_qword_if_in_range, Q bytes)."""
    with np.errstate(all="ignore"):
        x, y, z = (f32(c) for c in v)
        one = f32(1.0)
        P = []
        for j in range(4):
            acc = f32(f32(f32(x * f32(M[0][j])) + f32(y * f32(M[1][j]))) + f32(z * f32(M[2][j])))
            P.append(f32(f32(f32(M[3][j]) * one) + acc))
        Q = f32(one / P[3])
        X = cvtt(f32(f32(P[0] * Q) * f32(16.0)))
        Y = cvtt(f32(f32(P[1] * Q) * f32(16.0)))
        Z = cvtt(f32(P[2] * Q))
        qb = struct.pack("<f", f32(one * Q))
    ok = all(lo <= c <= hi for c, (lo, hi) in zip((X, Y, Z), bounds))
    entry = (X | (Y << 16) | (Z << 32) | (0xFF << 56)) & 0xFFFFFFFFFFFFFFFF if ok else None
    return ok, entry, qb


IDENT = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
EDGE = [("in (100,200,1000)", (100.0, 200.0, 1000.0)),
        ("X < 0 (x = -1)", (-1.0, 200.0, 1000.0)),
        ("X truncates to 0 (x = -0.03)", (-0.03, 200.0, 1000.0)),
        ("X = 0xFFF0, Y = 0, Z = 0xFF", (4095.0, 0.0, 255.0)),
        ("X = 0xFFF1", (4095.0625, 0.0, 255.0)),
        ("Z = 0xFE", (1.0, 1.0, 254.0)),
        ("Z = 0xFFFFFF", (1.0, 1.0, 16777215.0)),
        ("Z = 0x1000000", (1.0, 1.0, 16777216.0)),
        ("X = NaN", (float("nan"), 1.0, 1000.0)),
        ("Y = 80000", (1.0, 5000.0, 1000.0))]


def le(q):
    return struct.unpack("<Q", q)[0]


def exec_t1_edges(bench, R, label="E1"):
    """0039A150 on the edge set: in-range -> model qword; out-of-range -> 0; second qword untouched."""
    bench.set_matrix(IDENT)
    vs = [v for _, v in EDGE]
    eax, first, second, q = bench.run(T1S, vs)
    rows, ok = [], True
    for (nm, v), fq, sq, qq in zip(EDGE, first, second, q):
        inr, ent, qb = model(IDENT, v)
        want = ent if inr else 0
        good = le(fq) == want and sq == b"\xA5" * 8 and qq == qb
        ok &= good
        rows.append("%s: %s %016X" % (nm, "in " if inr else "OUT", le(fq)))
    R.check("%s 0039A150 executed on 10 edge vertices (identity rows, w = 1): each in-range vertex's entry is "
            "X | Y<<16 | Z<<32 | 0xFF<<56, each out-of-range vertex's entry first qword is 0; the second qword is "
            "never written; Q = 1.0 stored for every vertex; eax = 1" % label,
            ok and eax == 1, "; ".join(rows))
    return first


def section_e(img, R):
    print("== E: the original bytes executed (Unicorn); inputs: vertices (x, y, z, 1.0) at 0x10000000, entries "
          "prefilled 0xA5 at 0x10010000, Q prefilled 0x5A at 0x10020000, count = number of vertices; rows 1-4 "
          "(022D91B0) written directly; $zero left at its load value 0")
    bench = Bench(img)
    for nm, v in EDGE:
        inr, ent, _ = model(IDENT, v)
        R.note("   %-30s model: %s%s" % (nm, "in range" if inr else "OUT of range", (" %016X" % ent) if inr else ""))
    exec_t1_edges(bench, R)
    vs = [v for _, v in EDGE]
    eax, first, second, q = bench.run(T0S, vs)
    inr0, ent0, qb0 = model(IDENT, vs[0])
    R.check("E2 00399B80 on the same 10: returns 1 at vertex 1 (the first out-of-range one); entry 0 = the model "
            "qword; entries 1-9 untouched; Q written for vertices 0 and 1 only (the Q store precedes the compare)",
            eax == 1 and le(first[0]) == ent0 and all(f == b"\xA5" * 8 for f in first[1:]) and
            q[0] == qb0 and q[1] == model(IDENT, vs[1])[2] and all(x == b"\x5A" * 4 for x in q[2:]),
            "eax %d entry0 %016X" % (eax, le(first[0])))
    ins = [v for _, v in EDGE if model(IDENT, v)[0]]
    eax, first, second, q = bench.run(T0S, ins)
    eax1, first1, _, _ = bench.run(T1S, ins)
    R.check("E3 on the %d in-range edge vertices alone 00399B80 returns 0 and writes every entry, bit-identical to "
            "0039A150's and to the model" % len(ins),
            eax == 0 and first == first1 and all(le(f) == model(IDENT, v)[1] for f, v in zip(first, ins)))
    late = ins + [EDGE[1][1]]
    eax, first, _, _ = bench.run(T0S, late)
    R.check("E4 with the out-of-range vertex moved last, 00399B80 still returns 1, after writing all %d earlier "
            "entries (the reject is per vertex, at whichever vertex fails)" % len(ins),
            eax == 1 and all(le(f) == model(IDENT, v)[1] for f, v in zip(first[:-1], ins)) and first[-1] == b"\xA5" * 8)

    # random: a perspective-like matrix with off-diagonal noise (w ~ z); vertices with w > 0 and w < 0
    rnd = random.Random(199)
    M = [(800.0, rnd.uniform(-20, 20), rnd.uniform(-5, 5), rnd.uniform(-0.01, 0.01)),
         (rnd.uniform(-20, 20), 800.0, rnd.uniform(-5, 5), rnd.uniform(-0.01, 0.01)),
         (2048.0, 2048.0, 100000.0, 1.0),
         (rnd.uniform(-50, 50), rnd.uniform(-50, 50), -400000.0, rnd.uniform(-0.2, 0.2))]
    bench.set_matrix(M)
    n_in = n_out = n_behind_in = 0
    bad1 = bad0 = 0
    for b in range(40):
        vs = []
        for _ in range(50):
            z = rnd.choice([rnd.uniform(0.3, 60.0), rnd.uniform(-60.0, -0.3)])
            vs.append((rnd.uniform(-4, 4) * abs(z), rnd.uniform(-4, 4) * abs(z), z))
        eax, first, second, q = bench.run(T1S, vs)
        for v, fq, sq, qq in zip(vs, first, second, q):
            inr, ent, qb = model(M, v)
            n_in += inr
            n_out += not inr
            n_behind_in += inr and v[2] < 0
            if le(fq) != (ent if inr else 0) or sq != b"\xA5" * 8 or qq != qb:
                bad1 += 1
        for v in vs[:10]:
            eax0, f0, _, _ = bench.run(T0S, [v])
            inr, ent, _ = model(M, v)
            if eax0 != (0 if inr else 1) or (inr and le(f0[0]) != ent) or (not inr and f0[0] != b"\xA5" * 8):
                bad0 += 1
    R.check("E5 2,000 random vertices through 0039A150 (40 calls x 50): every entry equals the model (in range: "
            "packed XYZF with F = 0xFF; out of range: 0), bit-exact; %d in range, %d out" % (n_in, n_out),
            bad1 == 0 and n_in > 200 and n_out > 200, "%d mismatches" % bad1)
    R.check("E6 400 of them one at a time through 00399B80: it returns 1 exactly when the model says out of range, "
            "and otherwise writes the same qword", bad0 == 0, "%d mismatches" % bad0)
    R.note("   %d of the in-range vertices have w < 0 (here z < 0): the test is a range test on the "
           "projected integers, not a frustum test" % n_behind_in)
    return bench


# ============================================================================================== C
def section_c(img, R):
    print("== C: controls")
    # C1: a 0039A150 whose unequal arm stores the flag value (rax) instead of $zero must fail E1
    assert img.read(0x39A6CD, 3) == b"\x49\x89\x0b"
    P1 = img.patched(0x39A6CD, b"\x49\x89\x03")       # mov qword ptr [r11], rax
    Rq = Report("c1")
    Rq.quiet = True
    exec_t1_edges(Bench(P1), Rq)
    R.check("C1 control: on a patched image whose unequal arm stores rax (the non-zero compare value) instead of "
            "$zero, E1 FAILS", Rq.fails > 0)
    # C2: a model with the wrong bounds (X,Y max 0xFFFF, Z min 0) must disagree with the executed bytes
    bench = Bench(img)
    bench.set_matrix(IDENT)
    probe = [(4095.5, 1.0, 1000.0), (1.0, 1.0, 128.0)]
    eax, first, _, _ = bench.run(T1S, probe)
    wrong = ((0, 0xFFFF), (0, 0xFFFF), (0, 0xFFFFFF))
    agree_wrong = all(le(f) == ((model(IDENT, v, wrong)[1]) or 0) for f, v in zip(first, probe))
    agree_right = all(le(f) == ((model(IDENT, v)[1]) or 0) for f, v in zip(first, probe))
    R.check("C2 control: a model with X,Y max 0xFFFF and Z min 0 disagrees with the executed bytes on X = 0xFFF8 "
            "and Z = 0x80, which the stated bounds predict (entries %s)" % [("%016X" % le(f)) for f in first],
            agree_right and not agree_wrong)
    # C3: the writer sweep finds a planted writer of $zero
    assert img.read(0x39A0F9, 3) == b"\x4c\x8b\x15"
    P3 = img.patched(0x39A0F9, b"\x4c\x89\x15")       # mov qword ptr [rip -> 022D8F10], r10
    w, _, _ = zero_writers(P3)
    R.check("C3 control: on a patched image where 0039A0F9 stores r10 to 022D8F10, the Z1 sweep reports that writer",
            [x[0] for x in w] == [0x39A0F9], str(w))


def main():
    img = Img.load()
    img.cs.detail = True
    R = Report("sd199b")
    section_s(img, R)
    section_z(img, R)
    section_b(img, R)
    section_e(img, R)
    section_c(img, R)
    print("FAILS %d" % R.fails)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
