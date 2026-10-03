"""check_s01.py - FABLE, 2026-10-03: executed check for the S-01 section "4a. The archive mount and the startup latch".

Static part (rvlib/capstone + rawref.py raw index over .text, .rdata and .data):
  V   the GameApplication vtable 008C5760: slots 2, 3, 4, 7, 8
  F   the framework's init 0079F150 calls slot 2 then slot 3 through the vtable and stops on a non-zero return
  M   slot 2 0017CEB0: stores its two arguments, sets the content root, ensures the mount context, mounts
      '../FFXII_TZA.vbf', discards the mount result and returns 0 on its only exit
  K   the mount 0019B070: five context slots, failure clears the slot; the open 001F4340's accept/reject tests
  J   slot 3 0017CF30 ensures the AsyncJobManager pair (only caller of 0019A0A0) and posts {0017D150, this};
      0017D150 is `jmp 0017D000`; the worker 0019A1A0 polls with Sleep(5) and calls the job's function
  W   0017D000 stores +0x113C = 1 as its last store, after 0017D4C0 / 00210EC0(0x80) / 0018A840 / 00189000
  L   the latch census: [reg+0x113C] any width, any access overlapping +0x113C from +0x1130..+0x113B, and every
      rip / image-base-relative reference to the static object's cells 01F7F488..01F7F48F
  R   the readers: what each does when the latch is clear
Executed part (Unicorn 2.1.4):
  X1  slots 4 and 8 with the latch clear return 0 without entering any callee; slot 8 with the latch set calls
      the renderer getter 00189120; slot 7 with the latch clear and [01FD4948] = 0 enters no callee but 00228480
  U1  the original open 001F4340, run on the SHIPPED archive ../FFXII_TZA.vbf through import stubs that perform
      the real file reads and an MD5 (CALG_MD5 0x8003 asserted), reaches the accept point 001F453B
  U2..U4 sensitivity: a header byte flipped in the read buffer, a wrong magic, and a missing file each reach the
      reject point 001F4705 (U3 also prints "BigFile head wrong!" and leaves its FILE open)
Controls (each must FAIL the check it targets):
  C1  an image whose latch store is retargeted to +0x113D: the L census must no longer find one [reg] writer
  C2  an image whose magic immediate is changed: U1 must reject the shipped archive
  C3  an image whose slot 2 `xor eax, eax` is replaced by `mov eax, esi`: M must no longer prove "returns 0"
Prints FAILS N last.
"""
import hashlib
import os
import struct
import sys

from rawref import Img, text_refs, data_refs, disp_sweep, decode_fn
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
VBF_DIR_CANDIDATES = [r"D:\FFXII MP Mod\FFXII_TestClient1\x64", r"D:\FFXII MP Mod\FFXII_TestClient2\x64"]

FAILS = [0]


def report(tag, ok, text, quiet=False, sink=None):
    if sink is not None:
        sink.append(bool(ok))
        return bool(ok)
    FAILS[0] += not ok
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", tag, text))
    return bool(ok)


def lin(img, s, e):
    return [ci for ci in img.cs.disasm(img.read(s, e - s), s)]


def txt(ci):
    return (ci.mnemonic + " " + ci.op_str).strip()


def at(img, va):
    return txt(next(img.cs.disasm(img.read(va, 16), va)))


# ---------------------------------------------------------------- static checks
def check_vtable(img, R=None):
    VT = 0x008C5760
    want = {2: 0x0017CEB0, 3: 0x0017CF30, 4: 0x0017CCD0, 7: 0x0017CE50, 8: 0x0017D090}
    got = dict((k, img.u64(VT + 8 * k)) for k in want)
    return report("V1", got == want, "vtable 008C5760 slots 2/3/4/7/8 = %s" % (
        ", ".join("%d:%08X" % (k, got[k]) for k in sorted(got))), sink=R)


def check_framework(img, R=None):
    ok = at(img, 0x0079F591) == "call qword ptr [rax + 0x10]" and at(img, 0x0079F598) == "je 0x79f5bc" \
        and at(img, 0x0079F69A) == "call qword ptr [rax + 0x18]" and at(img, 0x0079F6A1) == "je 0x79f6c2"
    s = img.read(0x01CB2CD8, 40).split(b"\0")[0]
    ok2 = s.startswith(b"App failed during initApplication") and \
        img.read(0x01CB2D28, 30).startswith(b"App failed during initScene")
    r1 = report("F1", ok, "0079F150 calls slot 2 ([rax+0x10], 0079F591) then slot 3 ([rax+0x18], 0079F69A); "
                "each non-zero return leaves init (0079F598 / 0079F6A1)", sink=R)
    r2 = report("F2", ok2, "the two failure strings are initApplication (01CB2CD8) and initScene (01CB2D28)", sink=R)
    refs, _ = text_refs(img, 0x0079F150)
    r3 = report("F3", [r["site"] for r in refs] == [0x0079E5ED], "0079F150's only .text reference is 0079E5ED (in "
                "0079E520): %s" % ["%08X" % r["site"] for r in refs], sink=R)
    return r1 and r2 and r3


def check_mount(img, R=None):
    body = lin(img, 0x0017CEB0, 0x0017CF28)
    T = dict((ci.address, txt(ci)) for ci in body)
    rets = [ci.address for ci in body if ci.mnemonic == "ret"]
    jumps = [ci.address for ci in body if ci.mnemonic.startswith("j")]
    eax_writes = [ci.address for ci in body if ci.address > 0x0017CF11 and
                  any(r in ("eax", "rax") for r in [ci.reg_name(x) for x in ci.regs_access()[1]])]
    ok = T.get(0x0017CEC2) == "mov qword ptr [rcx + 0x1130], rdx" and \
        T.get(0x0017CEC9) == "mov dword ptr [rcx + 0x1138], r8d" and \
        T.get(0x0017CEDD) == "call 0x59a770" and T.get(0x0017CEE2) == "call 0x19b190" and \
        T.get(0x0017CEE7) == "call 0x19b1f0" and T.get(0x0017CEF6) == "call 0x19b070" and \
        T.get(0x0017CF00) == "call 0x17d6b0" and T.get(0x0017CF11) == "call 0x182f70"
    r1 = report("M1", ok, "slot 2 stores rdx -> +0x1130 (0017CEC2), r8d -> +0x1138 (0017CEC9), then calls 0059A770, "
                "0019B190, 0019B1F0, 0019B070, 0017D6B0, 00182F70", sink=R)
    s1 = img.read(0x008C5858, 16).split(b"\0")[0]
    s2 = img.read(0x008C5868, 24).split(b"\0")[0]
    r2 = report("M2", s1 == b"../../.." and s2 == b"../FFXII_TZA.vbf" and
                at(img, 0x0059A770) == "mov qword ptr [rip + 0x270f609], rcx",
                "'../../..' (008C5858) is stored by 0059A770 into 02CA9D80; '../FFXII_TZA.vbf' (008C5868) is the "
                "mount path", sink=R)
    r3 = report("M3", not jumps and rets == [0x0017CF27] and eax_writes == [0x0017CF1B] and
                T.get(0x0017CF1B) == "xor eax, eax" and T.get(0x0017CEFB) == "mov rdx, rbx",
                "slot 2 has no branch, one ret (0017CF27), and its only eax write after the last call is "
                "`xor eax, eax` (0017CF1B); the mount's al is not tested (0017CEFB)", sink=R)
    r4 = report("M4", at(img, 0x0019B1F0) == "mov rax, qword ptr [rip + 0x1de5f19]" and
                at(img, 0x0019B19F) == "cmp qword ptr [rip + 0x1de5f69], 0",
                "the mount context is the 0x80-byte singleton [01F81110] (ensure 0019B190, getter 0019B1F0)", sink=R)
    return r1 and r2 and r3 and r4


def check_open(img, R=None):
    T = dict((ci.address, txt(ci)) for ci in lin(img, 0x0019B070, 0x0019B12F))
    ok = T.get(0x0019B0A7) == "cmp r8, 5" and T.get(0x0019B0AD) == "jmp 0x19b11d" and \
        T.get(0x0019B0E5) == "call 0x1f4340" and T.get(0x0019B10F) == "mov qword ptr [rdi + 0x20], 0" and \
        T.get(0x0019B0B4) == "call 0x210ec0" and T.get(0x0019B11D) == "xor al, al"
    r1 = report("K1", ok, "0019B070: five slots at +0x20..+0x47 (0019B0A7), none free -> al 0 (0019B0AD); open "
                "001F4340 (0019B0E5); a failed open clears the slot (0019B10F)", sink=R)
    O = dict((ci.address, txt(ci)) for ci in lin(img, 0x001F4340, 0x001F471F))
    ok2 = O.get(0x001F43D7) == "cmp dword ptr [rbp + 0x50], 0x4b595253" and \
        O.get(0x001F44AB) == "mov edx, 0x8003" and O.get(0x001F4407) == "mov dword ptr [rbp + 0x58], 0x10" and \
        O.get(0x001F4701) == "mov al, 1" and O.get(0x001F4705) == "xor al, al" and \
        O.get(0x001F43E7) == "call 0x17d280" and O.get(0x001F43EC) == "jmp 0x1f4705"
    r2 = report("K2", ok2, "001F4340: magic 'SRYK' (001F43D7), CALG_MD5 0x8003 (001F44AB), 16-byte digest "
                "(001F4407); accept al=1 (001F4701), reject al=0 (001F4705)", sink=R)
    # the bad-magic path: no fclose between the fopen and the reject
    fclose_sites = [a for a, t in O.items() if t == "call qword ptr [rip + 0x6cea89]"]
    r3 = report("K3", fclose_sites == [0x001F4471] and 0x001F4471 > 0x001F43EC,
                "001F4340's only fclose is 001F4471, after the magic test: the bad-magic exit (001F43EC) leaves the "
                "FILE open", sink=R)
    ok4 = O.get(0x001F4687) == "mov ecx, 0x2d8" and O.get(0x001F4695) == "mov esi, 0xf" and \
        O.get(0x001F46F2) == "call 0x215290" and at(img, 0x002152AD) == "call qword ptr [rip + 0x6adc45]"
    r4 = report("K4", ok4, "on accept 001F4340 builds 15 x 0x30 stream records (001F4687/001F4695) and 00215290 "
                "fopen()s the archive once more for each (002152AD), unchecked", sink=R)
    return r1 and r2 and r3 and r4


def check_job(img, R=None):
    T = dict((ci.address, txt(ci)) for ci in lin(img, 0x0017CF30, 0x0017CFC6))
    ok = T.get(0x0017CF77) == "call 0x19a0a0" and T.get(0x0017CF7C) == "call 0x19a170" and \
        T.get(0x0017CF84) == "call 0x199f10" and T.get(0x0017CF8C) == "lea rax, [rip + 0x1bd]" and \
        T.get(0x0017CF93) == "mov qword ptr [rbx], rax" and T.get(0x0017CF96) == "mov qword ptr [rbx + 8], rbp" and \
        T.get(0x0017CFA5) == "call 0x19a000" and T.get(0x0017CFC1) == "jmp 0x5c5230"
    r1 = report("J1", ok and 0x0017CF8C + 7 + 0x1BD == 0x0017D150,
                "slot 3: ensure 0019A0A0 (0017CF77), get [01F810F8] (0017CF7C), pool node 00199F10 (0017CF84), "
                "{fn=0017D150, arg=this} (0017CF8C..96), enqueue 0019A000 (0017CFA5), tail 005C5230 (0017CFC1)", sink=R)
    refs, _ = text_refs(img, 0x0019A0A0)
    r2 = report("J2", [r["site"] for r in refs] == [0x0017CF77],
                "slot 3 is the only caller of the AsyncJobManager ensure 0019A0A0: %s" %
                ["%08X" % r["site"] for r in refs], sink=R)
    r3 = report("J3", at(img, 0x0017D150) == "jmp 0x17d000" and at(img, 0x005C5230) == "xor eax, eax",
                "0017D150 is `jmp 0017D000`; 005C5230 is `xor eax, eax; ret`", sink=R)
    W = dict((ci.address, txt(ci)) for ci in lin(img, 0x0019A1A0, 0x0019A299))
    imp = img.u64(0x008C21B0)                      # the IAT slot 005CCB80 jumps through
    sleep_name = img.read(img.base + imp + 2, 8).split(b"\0")[0]
    ok4 = W.get(0x0019A1D0) == "mov ecx, 5" and W.get(0x0019A1D5) == "call 0x5ccb80" and \
        sleep_name == b"Sleep" and W.get(0x0019A1FF) == "mov rax, qword ptr [rbp + 0x58]" and \
        W.get(0x0019A246) == "mov rcx, qword ptr [rsi + 8]" and W.get(0x0019A24A) == "call rax" and \
        W.get(0x0019A27E) == "jne 0x19a1d0"
    r4 = report("J4", ok4, "worker 0019A1A0: Sleep(5) per pass (0019A1D0/0019A1D5 -> 005CCB80 -> Sleep), takes the "
                "oldest node ([+0x58], 0019A1FF), calls fn(arg) (0019A246/0019A24A), loops while +0x154 (0019A27E)",
                sink=R)
    C = dict((ci.address, txt(ci)) for ci in lin(img, 0x00199F60, 0x00199FF6))
    ct = dict((ci.address, txt(ci)) for ci in lin(img, 0x005CD1E0, 0x005CD240))
    ct_imp = img.read(img.base + img.u64(0x005CD228 + 6 + struct.unpack("<i", img.read(0x005CD228 + 2, 4))[0]) + 2,
                      16).split(b"\0")[0]
    ok5 = C.get(0x00199F84) == "lea rdx, [rip + 0x205]" and 0x00199F84 + 7 + 0x205 == 0x0019A190 and \
        at(img, 0x0019A190) == "jmp 0x19a1a0" and C.get(0x00199FE7) == "call 0x5cd1e0" and ct_imp == b"CreateThread" \
        and img.read(0x008F3C70, 24).startswith(b"AsyncJobManager Thread") and \
        at(img, 0x0019A0D3) == "call 0x1999d0" and at(img, 0x00199A62) == "call 0x199f60" and \
        at(img, 0x0019A0DA) == "mov rax, rbx" and at(img, 0x0019A0DD) == "mov qword ptr [rip + 0x1de7014], rax"
    r5 = report("J5", ok5, "ensure 0019A0A0 -> ctor 001999D0 (0019A0D3) -> 00199F60 (00199A62) starts thread proc "
                "0019A190 -> 0019A1A0 through 005CD1E0 (CreateThread at 005CD228), 'AsyncJobManager Thread' "
                "(008F3C70); a failed allocation stores NULL to 01F810F8 (0019A0DA/0019A0DD)", sink=R)
    return r1 and r2 and r3 and r4 and r5


def check_writer(img, R=None):
    body = lin(img, 0x0017D000, 0x0017D081)
    T = dict((ci.address, txt(ci)) for ci in body)
    order = [T.get(a) for a in (0x0017D01F, 0x0017D029, 0x0017D03B, 0x0017D06F, 0x0017D074)]
    want = ["call 0x17d4c0", "call 0x210ec0", "call 0x18a840", "call 0x189000", "mov byte ptr [rbx + 0x113c], 1"]
    after = [ci for ci in body if ci.address > 0x0017D074]
    stores_after = [ci for ci in after if any(op.type == X86_OP_MEM for op in ci.operands) and
                    ci.mnemonic not in ("pop", "ret", "add")]
    jcc = [(ci.address, txt(ci)) for ci in body if ci.mnemonic.startswith("j")]
    ok = order == want and not stores_after and jcc == [(0x0017D036, "je 0x17d041")]
    return report("W1", ok, "0017D000: 0017D4C0 (0017D01F), alloc 0x80 (0017D029), 0018A840 (0017D03B), 00189000 "
                  "(0017D06F), then +0x113C = 1 (0017D074), its last memory write; its one branch (0017D036) "
                  "rejoins before the store", sink=R)


def check_census(img, R=None):
    w = [x for x in disp_sweep(img, 0x113C)]
    regs = [(x[0], x[1]) for x in w if "rsp" not in x[1]]
    want = [(0x0017CCD6, "cmp byte ptr [rcx + 0x113c], 0"), (0x0017CE77, "cmp byte ptr [rbx + 0x113c], 0"),
            (0x0017D074, "mov byte ptr [rbx + 0x113c], 1"), (0x0017D094, "cmp byte ptr [rcx + 0x113c], 0")]
    r1 = report("L1", regs == want, "[reg+0x113C], any width, image-wide: %d sites (1 write, 3 reads): %s" % (
        len(regs), ["%08X" % a for a, _ in regs]), sink=R)
    over = []
    for d in range(0x1130, 0x113C):
        for x in disp_sweep(img, d):
            if d + x[2] > 0x113C and "rsp" not in x[1]:
                over.append((x[0], x[1]))
    r2 = report("L2", not over, "no non-stack access from +0x1130..+0x113B reaches +0x113C: %s" % over, sink=R)
    refs, unc = text_refs(img, 0x01F7F488, 0x01F7F490)
    got = [(r["site"], r["text"]) for r in refs]
    r3 = report("L3", (0x0015BC68, "mov word ptr [rip + 0x1e2381b], 0") in got and
                [g for g in got if g[0] != 0x0017D24A] == [(0x0015BC68, "mov word ptr [rip + 0x1e2381b], 0")] and
                0x0015BC68 + 9 + 0x1E2381B == 0x01F7F48C == 0x01F7E350 + 0x113C,
                "rip refs to the static object's 01F7F488..01F7F48F: the constructor's word clear of +0x113C/+0x113D "
                "(0015BC68 -> 01F7F48C) and %s" % ["%08X %s" % g for g in got if g[0] != 0x0015BC68], sink=R)
    base, _ = text_refs(img, 0x01F7E350, 0x01F7E358)
    r4 = report("L4", [r["site"] for r in base] == [0x0015BC4D, 0x0015BC61, 0x0015BC76, 0x00896280, 0x008A6977,
                                                    0x008A697E] and
                at(img, 0x0015BC5A) == "lea rax, [rip + 0x769aff]" and at(img, 0x00896287) == "jmp 0x793250" and
                at(img, 0x008A6985) == "jmp 0x793250" and at(img, 0x0015BCB7) == "lea rcx, [rip + 0x74acb2]" and
                not data_refs(img, 0x01F7E350, 0x01F7E351),
                "the static GameApplication 01F7E350 is named in .text only by its constructor 0015BC40 (3 sites; "
                "vtable 008C5760 at 0015BC5A), the constructor's unwind funclet 00896280 and the atexit destructor "
                "008A6970 (registered at 0015BCB7); both of the latter only run the base destructor 00793250", sink=R)
    pair, _ = text_refs(img, 0x01F7F480, 0x01F7F48C)
    got = [(r["site"], r["text"]) for r in pair]
    callers, _ = text_refs(img, 0x0017D240)
    r5 = report("L5", got == [(0x0017D240, "mov rax, qword ptr [rip + 0x1e02239]"),
                              (0x0017D24A, "mov eax, dword ptr [rip + 0x1e02238]")] and
                [r["site"] for r in callers] == [0x00408C6A],
                "slot 2's stored pair +0x1130/+0x1138 is also read rip-relative by the getter 0017D240 (0017D240, "
                "0017D24A), whose one caller is the FF12CONFIG loader 00408C30 (00408C6A)", sink=R)
    body = lin(img, 0x00792350, 0x00792690)
    rsi_w = [ci.address for ci in body if 0x00792370 < ci.address < 0x00792550 and
             "rsi" in [ci.reg_name(x) for x in ci.regs_access()[1]]]
    r6 = report("L6", at(img, 0x0015BC54) == "call 0x792350" and at(img, 0x0015BC4D) == "lea rcx, [rip + 0x1e226fc]"
                and at(img, 0x00792370) == "mov rsi, rcx" and not rsi_w and
                at(img, 0x00792550) == "mov qword ptr [rip + 0x2712e11], rsi" and 0x00792557 + 0x2712E11 == 0x02EA5368
                and img.u64(0x008C31F0) == 0x0015BC40 and
                [d[1] for d in data_refs(img, 0x0015BC40, 0x0015BC41) if d[2] == "va64"] == [0x008C31F0],
                "the constructor 0015BC40 (whose only pointer is .rdata 008C31F0) passes 01F7E350 to the base ctor "
                "00792350, which publishes it to the handle 02EA5368 (00792550; rsi = this, unchanged since "
                "00792370)", sink=R)
    return r1 and r2 and r3 and r4 and r5 and r6


def check_readers(img, R=None):
    S4 = dict((ci.address, txt(ci)) for ci in lin(img, 0x0017CCD0, 0x0017CDBD))
    ok4 = S4.get(0x0017CCD6) == "cmp byte ptr [rcx + 0x113c], 0" and S4.get(0x0017CCE0) == "je 0x17cd84" and \
        S4.get(0x0017CD89) == "jmp 0x5c5230"
    S7 = dict((ci.address, txt(ci)) for ci in lin(img, 0x0017CE50, 0x0017CEA7))
    ok7 = S7.get(0x0017CE59) == "call 0x228480" and S7.get(0x0017CE60) == "je 0x17ce77" and \
        S7.get(0x0017CE6A) == "call 0x1967d0" and S7.get(0x0017CE77) == "cmp byte ptr [rbx + 0x113c], 0" and \
        S7.get(0x0017CE95) == "call 0x16d6a0" and at(img, 0x0016D6A0) == "ret 0" and \
        at(img, 0x00228482) == "cmp qword ptr [rip + 0x1dac4bf], rax"
    S8 = dict((ci.address, txt(ci)) for ci in lin(img, 0x0017D090, 0x0017D0B5))
    ok8 = S8.get(0x0017D094) == "cmp byte ptr [rcx + 0x113c], 0" and S8.get(0x0017D09D) == "xor eax, eax" and \
        S8.get(0x0017D0B0) == "jmp 0x187950"
    r1 = report("R1", ok4, "slot 4: latch clear -> 0017CD84 -> tail 005C5230 (returns 0)", sink=R)
    r2 = report("R2", ok7, "slot 7: 00228480 ([01FD4948] != 0) arm runs BEFORE the latch test (0017CE59..6A, "
                "input 001967D0); the latched arm's only call is 0016D6A0 = `ret 0` (0017CE95)", sink=R)
    def imp_at(site):
        ci = next(img.cs.disasm(img.read(site, 16), site))
        slot = site + ci.size + ci.operands[0].mem.disp
        return img.read(img.base + img.u64(slot) + 2, 24).split(b"\0")[0]
    report("O1", imp_at(0x005CD236) == b"GetLastError" and imp_at(0x005CD262) == b"FormatMessageA" and
           imp_at(0x005CD2D8) == b"RaiseException" and at(img, 0x005CD2CF) == "mov ecx, 0x406d1388" and
           S4.get(0x0017CCF0) == "movsd xmm6, qword ptr [rcx + 0x48]",
           "Open-list sites: 005CD236 GetLastError, 005CD262 FormatMessageA, 005CD2D8 RaiseException(0x406D1388 at "
           "005CD2CF); slot 4 reads +0x48 at 0017CCF0", sink=R)
    r3 = report("R3", ok8, "slot 8: latch clear -> return 0 (0017D09D); set -> render pass list 00187950 (0017D0B0)",
                sink=R)
    return r1 and r2 and r3


# ---------------------------------------------------------------- unicorn
def uc_image(img):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_PROT_ALL
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    lo = img.base
    hi = max(img.base + va + vs for _, va, vs, _, _ in img.secs)
    hi = (hi + 0xFFFF) & ~0xFFFF
    uc.mem_map(lo, hi - lo, UC_PROT_ALL)
    uc.mem_write(lo, img.d[:0x1000])
    for name, va, vs, ra, rs in img.secs:
        uc.mem_write(lo + va, img.d[ra:ra + min(vs, rs)])
    uc.mem_map(0x10000000, 0x100000)       # stack
    uc.mem_map(0x20000000, 0x4000000)      # heap (bump)
    uc.mem_map(0x30000000, 0x1000)         # import stubs
    return uc


def run_slot(img, fn, latch, gate=0):
    """Run slot fn on the static object with the latch byte = latch; return (eax, callees entered)."""
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RAX, UC_X86_REG_RIP
    uc = uc_image(img)
    this = 0x01F7E350
    uc.mem_write(this + 0x113C, bytes([latch]))
    uc.mem_write(0x01FD4948, struct.pack("<Q", gate))
    entered = []
    RET = 0x30000800
    s, e = fn, {0x0017CCD0: 0x0017CDBD, 0x0017CE50: 0x0017CEA7, 0x0017D090: 0x0017D0B5}[fn]

    def hook(u, addr, size, _):
        if addr == RET:
            u.emu_stop()
            return
        if not (s <= addr < e) and addr not in (0x005C5230, 0x005C5232):
            entered.append(addr)
            u.emu_stop()
    uc.hook_add(UC_HOOK_CODE, hook)
    sp = 0x10080000
    uc.mem_write(sp, struct.pack("<Q", RET))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, this)
    uc.reg_write(UC_X86_REG_RAX, 0x5A5A5A5A)
    uc.emu_start(fn, RET, count=10000)
    return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF, entered


def check_slots_exec(img, R=None):
    a4, c4 = run_slot(img, 0x0017CCD0, 0)
    a8, c8 = run_slot(img, 0x0017D090, 0)
    b8, d8 = run_slot(img, 0x0017D090, 1)
    a7, c7 = run_slot(img, 0x0017CE50, 0, 0)
    r1 = report("X1", a4 == 0 and not c4, "executed: slot 4, latch 0 -> eax %d, callees entered %s" % (
        a4, ["%08X" % x for x in c4]), sink=R)
    r2 = report("X2", a8 == 0 and not c8 and d8[:1] == [0x00189120], "executed: slot 8, latch 0 -> eax %d, callees %s; "
                "latch 1 -> first callee %s" % (a8, ["%08X" % x for x in c8], ["%08X" % x for x in d8[:1]]), sink=R)
    r3 = report("X3", c7 == [0x00228480], "executed: slot 7, latch 0 -> first callee %s (the ungated test runs "
                "first)" % ["%08X" % x for x in c7], sink=R)
    return r1 and r2 and r3


def find_vbf():
    for d in VBF_DIR_CANDIDATES:
        p = os.path.normpath(os.path.join(d, "..", "FFXII_TZA.vbf"))
        if os.path.exists(p):
            return d
    return None


def run_open(img, cwd, mutate=None):
    """Execute 001F4340(archive, '../FFXII_TZA.vbf') with import stubs. mutate: None | 'flip' | 'magic' | 'missing'.
    Returns dict(outcome='accept'|'reject'|..., prints=[...], opens=n, closes=n, alg=...)."""
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
                                   UC_X86_REG_RAX, UC_X86_REG_RIP)
    uc = uc_image(img)
    st = {"heap": 0x20000000, "files": {}, "next": 1, "prints": [], "opens": 0, "closes": 0, "alg": None,
          "md5": None, "outcome": None, "freads": 0}
    STUB = 0x30000000
    imports = {0x008C2EF8: "fopen", 0x008C2EF0: "fread", 0x008C2E38: "_fseeki64", 0x008C2EE8: "fseek",
               0x008C2F00: "fclose", 0x008C2000: "CryptAcquireContextW", 0x008C2048: "CryptCreateHash",
               0x008C2040: "CryptHashData", 0x008C2010: "CryptGetHashParam", 0x008C2038: "CryptDestroyHash",
               0x008C2008: "CryptReleaseContext"}
    stub_of = {}
    for i, (slot, name) in enumerate(sorted(imports.items())):
        hn = img.u64(slot)
        assert img.read(img.base + hn + 2, 32).split(b"\0")[0].decode() == name, name
        addr = STUB + 0x10 * i
        stub_of[addr] = name
        uc.mem_write(slot, struct.pack("<Q", addr))
    stub_of[0x00210EC0] = "malloc"
    stub_of[0x0017D280] = "print"

    def rd(r):
        return uc.reg_read(r)

    def cstr(a):
        return bytes(uc.mem_read(a, 260)).split(b"\0")[0]

    def ret(val):
        sp = uc.reg_read(UC_X86_REG_RSP)
        ra = struct.unpack("<Q", bytes(uc.mem_read(sp, 8)))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RAX, val)
        uc.reg_write(UC_X86_REG_RIP, ra)

    def hook(u, addr, size, _):
        if addr == 0x001F453B:
            st["outcome"] = "accept"
            u.emu_stop()
            return
        if addr == 0x001F4705:
            st["outcome"] = "reject"
            u.emu_stop()
            return
        name = stub_of.get(addr)
        if name is None:
            return
        rcx, rdx, r8, r9 = rd(UC_X86_REG_RCX), rd(UC_X86_REG_RDX), rd(UC_X86_REG_R8), rd(UC_X86_REG_R9)
        sp = rd(UC_X86_REG_RSP)
        if name == "malloc":
            p = st["heap"]
            st["heap"] = (p + rcx + 0x3F) & ~0xF
            ret(p)
        elif name == "print":
            st["prints"].append(cstr(rcx))
            ret(0)
        elif name == "fopen":
            path = cstr(rcx).decode()
            full = os.path.normpath(os.path.join(cwd, path))
            if mutate == "missing":
                full = full + ".absent"
            st["opens"] += 1
            if not os.path.exists(full):
                ret(0)
                return
            h = 0x7000 + st["next"]
            st["next"] += 1
            st["files"][h] = open(full, "rb")
            ret(h)
        elif name == "fread":
            f = st["files"][r9]
            n = rdx * r8
            b = f.read(n)
            st["freads"] += 1
            if mutate == "magic" and st["freads"] == 1:
                b = b"SRYX"[:len(b)]
            if mutate == "flip" and len(b) > 4096 and st["freads"] == 4:
                b = b[:1000] + bytes([b[1000] ^ 1]) + b[1001:]
            uc.mem_write(rcx, b)
            ret(len(b) // rdx if rdx else 0)
        elif name in ("fseek", "_fseeki64"):
            off = rdx if rdx < (1 << 63) else rdx - (1 << 64)
            if name == "fseek":
                off = struct.unpack("<i", struct.pack("<I", rdx & 0xFFFFFFFF))[0]
            st["files"][rcx].seek(off, r8 & 0xFFFFFFFF)
            ret(0)
        elif name == "fclose":
            st["closes"] += 1
            st["files"].pop(rcx).close()
            ret(0)
        elif name == "CryptAcquireContextW":
            uc.mem_write(rcx, struct.pack("<Q", 0x5100))
            ret(1)
        elif name == "CryptCreateHash":
            st["alg"] = rdx & 0xFFFFFFFF
            st["md5"] = hashlib.md5()
            ph = struct.unpack("<Q", bytes(uc.mem_read(sp + 0x28, 8)))[0]
            uc.mem_write(ph, struct.pack("<Q", 0x5200))
            ret(1)
        elif name == "CryptHashData":
            st["md5"].update(bytes(uc.mem_read(rdx, r8 & 0xFFFFFFFF)))
            ret(1)
        elif name == "CryptGetHashParam":
            assert (rdx & 0xFFFFFFFF) == 2
            dg = st["md5"].digest()
            uc.mem_write(r8, dg)
            uc.mem_write(r9, struct.pack("<I", len(dg)))
            ret(1)
        else:
            ret(1)
    uc.hook_add(UC_HOOK_CODE, hook)
    arch = 0x20F00000
    uc.mem_write(arch, b"\0" * 0xB0)
    sp = 0x10080000
    uc.mem_write(sp, struct.pack("<Q", 0x30000F00))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, arch)
    uc.reg_write(UC_X86_REG_RDX, 0x008C5868)          # the authored '../FFXII_TZA.vbf' in .rdata
    try:
        uc.emu_start(0x001F4340, 0x30000F00, count=5000000)
    except Exception as ex:  # an unmapped access is an outcome, not a crash of the check
        st["outcome"] = st["outcome"] or ("fault %s" % ex)
    for f in st["files"].values():
        st["leaked"] = st.get("leaked", 0) + 1
        f.close()
    return st


def check_open_exec(img, R=None, only_accept=False):
    cwd = find_vbf()
    if cwd is None:
        return report("U0", False, "shipped archive not found next to %s" % VBF_DIR_CANDIDATES, sink=R)
    s1 = run_open(img, cwd)
    r1 = report("U1", s1["outcome"] == "accept" and s1["alg"] == 0x8003 and not s1["prints"] and
                s1["opens"] == 1 and s1["closes"] == 1,
                "executed 001F4340 on the shipped %s: %s (alg %s, opens %d, closes %d)" % (
                    os.path.normpath(os.path.join(cwd, "..", "FFXII_TZA.vbf")), s1["outcome"],
                    s1["alg"] and hex(s1["alg"]), s1["opens"], s1["closes"]), sink=R)
    if only_accept:
        return r1
    s2 = run_open(img, cwd, "flip")
    r2 = report("U2", s2["outcome"] == "reject" and not s2["prints"] and s2["closes"] == 1,
                "sensitivity: header byte 1000 flipped in the read buffer -> %s (no message; FILE closed before "
                "hashing)" % s2["outcome"], sink=R)
    s3 = run_open(img, cwd, "magic")
    r3 = report("U3", s3["outcome"] == "reject" and s3["prints"] == [b"BigFile head wrong!\n"] and
                s3["closes"] == 0 and s3.get("leaked") == 1,
                "sensitivity: magic 'SRYX' -> %s, prints %s, FILE left open (closes %d)" % (
                    s3["outcome"], s3["prints"], s3["closes"]), sink=R)
    s4 = run_open(img, cwd, "missing")
    r4 = report("U4", s4["outcome"] == "reject" and not s4["prints"] and s4["opens"] == 1,
                "sensitivity: fopen returns NULL -> %s, no message" % s4["outcome"], sink=R)
    return r1 and r2 and r3 and r4


def header_facts():
    cwd = find_vbf()
    p = os.path.normpath(os.path.join(cwd, "..", "FFXII_TZA.vbf"))
    with open(p, "rb") as f:
        h = f.read(16)
        hs, n = struct.unpack("<II", h[4:12])
        f.seek(0)
        md = hashlib.md5(f.read(hs)).hexdigest()
        f.seek(-16, 2)
        tr = f.read(16).hex()
    report("H1", h[:4] == b"SRYK" and md == tr,
           "shipped archive: magic %r, header %d bytes, %d entries, MD5(header) = trailer = %s" % (h[:4], hs, n, md))


def main():
    img = Img.load()
    print("FABLE check_s01 (S-01 archive mount and startup latch), EXE sha256 verified by rvlib")
    check_vtable(img)
    check_framework(img)
    check_mount(img)
    check_open(img)
    check_job(img)
    check_writer(img)
    check_census(img)
    check_readers(img)
    check_slots_exec(img)
    header_facts()
    check_open_exec(img)

    # ---- controls: each mutated image must make its target check FAIL
    def control(tag, va, newbytes, fn, what, **kw):
        bad = img.patched(va, newbytes)
        sink = []
        try:
            fn(bad, sink, **kw) if kw else fn(bad, sink)
            failed = not all(sink)
        except Exception as ex:
            failed = True
        report(tag, failed, "control: %s -> the check %s" % (what, "FAILS as required" if failed else "still PASSES"))

    # C1: 0017D074 c6833c11000001 -> c6833d11000001 (store +0x113D instead)
    control("C1", 0x0017D074, bytes.fromhex("c6833d11000001"), check_census, "latch store retargeted to +0x113D")
    # C2: magic immediate 0x4b595253 -> 0x4b595254
    control("C2", 0x001F43DA, struct.pack("<I", 0x4B595254), check_open_exec,
            "magic immediate changed to 0x4B595254", only_accept=True)
    # C3: slot 2's `xor eax, eax` (33 c0) -> `mov eax, esi` (8b c6)
    control("C3", 0x0017CF1B, bytes.fromhex("8bc6"), check_mount, "slot 2 returns esi instead of 0")
    print("FAILS %d" % FAILS[0])
    return 1 if FAILS[0] else 0


if __name__ == "__main__":
    sys.exit(main())
