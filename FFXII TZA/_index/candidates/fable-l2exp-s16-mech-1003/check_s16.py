"""check_s16.py - FABLE, 2026-10-03: S-16 range retirement, the return window and the keep-bank rotation.

Settles, at the bytes of the certified image (73461d08..., base 0x00120000), the claims of section.txt (I9-I12):

  K1  the trigger: 002350C0 has exactly one caller, 00234022 in BattleUnit_UpdateLifecycleAndCombatFrame 00233F70, on
      its ACTIVE branch with rcx = [unit+0x10]; 00233F70 is named only by `lea r13` at 00265A4F, stored at record +0x38
      (00265AA8) and called by the drive loop at 0025E222; the drive loop clears record +0x0D bit 6 at 0025E1AD and sets
      it at 0025E217 just before that call, and 002672F0 (the retire's first gate) returns exactly that bit.
  K2  002350C0's gate chain and mode split read as section.txt states (sites), and the two tunable sources: the global
      range 02089368 is written only by 0023A1D0 (verb 0x300B) and 0023A540 (43.0, verb 0x3053's reset), read only at
      00235205; the per-unit mode/threshold/anchor come from 00238FC0 (verb 0x3019), which stores +0x4C/+0x51 only for
      mode 2.
  K3  the retire action keeps its own mark: 002352A6 sets record bit 0 BEFORE BattleUnit_TeardownAndDespawn(unit, 1);
      the teardown's spawn-backed tail calls the record clear 00237080 (mask 0xFFFFFF7A) only when its second argument
      is 0 (00300F5D); of the ten teardown call sites only 002352B1 passes a constant 1 (the idle teardown 00234100 passes 0); the automatic
      selector admits a bit-0 entry before the cooldown test (002358B6-002358BB).
  K4  the return window 0208936C: two writers (00236A0D = 300 in 002368D0, 0023534A the setter), two readers (002337FA in
      the rotation, 00235330 the getter); the getter's only caller is verb wrapper 00510810 and the setter's only caller
      is verb wrapper 005107F0; no pointer constant names the cell.
  K5  the rotation 00233780 has exactly one caller, 00234423 in area initialisation 002342F0, reached on both arms of
      002343CB and after the reset route 00239960 (00234349); the field-history words, the stamp and the parity have
      the writers section.txt lists; the serializer stores only the two field words (00233529, 00233533).
  K6  executed (Unicorn 2.1.4, original code; 003148F0, __chkstk and memset answered by hooks): 00233780's two branches
      a. A->B->A inside the window: bank CONTENTS exchanged (pointers unchanged), parity flipped, counters untouched;
      b. elapsed == 30 x scale x window restores, +1 wipes (unsigned `ja`);
      c. a different field wipes: bank 2 <- bank 1, bank 1 zeroed, parity flipped, the 64 u16 counters of the NEW
         parity set to 1 and the other 64 untouched;
      d. the stamp later than the clock (wrapped difference) wipes;
      e. after the reset's -1 history no field id restores (the getter clamps to >= 0);
      f. a null bank pointer returns before the history shift and the stamp;
      g. scale 2.0 doubles the tick limit;
      h. "returning to the area you just left" (field == last) wipes unless last == previous.
  K7  executed (Unicorn 2.1.4, original code; 00313F60, 003272A0, 00320940, 00265020, 0031B810, 003273B0, the teardown
      and the unregister answered by hooks): 002350C0's two senses
      a. mode 0 and mode 3 return 0 and call nothing;
      b. mode 1 keeps the unit while the focus slot is nearer than the range, retires at >= the range;
      c. mode 1 with the range unset (0.0) retires at any distance;
      d. mode 1 ignores a near non-focus slot; with no eligible slot it keeps the unit;
      e. mode 2 retires when the leader is within (<=) the per-unit threshold, keeps beyond it;
      f. mode 2 keeps the unit when the anchor fetch fails or there is no leader;
      g. the inhibit bit 4, the opt-in bit, bkbi[5] == 0 and the status mask without the waiver each keep the unit;
      h. the action order: record bit 0 set, teardown(unit, 1) with bit 0 already set, unregister(unit, 0); returns 1;
      i. an unordered distance (NaN) retires in BOTH modes.

Sensitivity controls (each must make a check FAIL; the control PASSES when it does):
  S1  image: 00233803 `ja` -> `jg` (signed): K6d must fail.
  S2  image: 002337CD reads 02089370 (last) instead of 02089372 (previous): K6a must fail.
  S3  image: 002351B9 `jbe` -> `ja` (mode 2 sense inverted): K7e must fail.
  S4  image: 002352A9 `mov edx, 1` -> `mov edx, 0`: K7h must fail.
  S5  claim: "an unset range (0.0) never retires a unit standing 0.5 from the focus member": refuted by K7c's run.

Prints FAILS N last.
"""
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rawref import Img, text_refs, data_refs, decode_fn  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, __version__ as UC_VERSION  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,  # noqa: E402
                               UC_X86_REG_R9, UC_X86_REG_RSP, UC_X86_REG_RIP)

BANK1, BANK2 = 0x0208E690, 0x0208E698
LAST, PREV, STAMP = 0x02089370, 0x02089372, 0x02089374
WINDOW, RANGE = 0x0208936C, 0x02089368
PARITY, COUNTERS = 0x0208D454, 0x0208D354
TICKS, SCALE = 0x0208D45C, 0x01DFE0B8
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


def ins(img, va):
    ci = next(img.cs.disasm(img.read(va, 16), va, 1))
    return ci


def txt(img, va):
    ci = ins(img, va)
    return (ci.mnemonic + " " + ci.op_str).strip()


def target(ci):
    """rip-relative target of an instruction's memory operand, or None."""
    from capstone.x86 import X86_OP_MEM, X86_REG_RIP
    for op in ci.operands:
        if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
            return ci.address + ci.size + op.mem.disp
    return None


def is_write(img, site):
    from capstone.x86 import X86_OP_MEM
    ci = ins(img, site)
    op0 = ci.operands[0] if ci.operands else None
    return bool(op0 is not None and op0.type == X86_OP_MEM and ci.mnemonic not in NOT_DEST_WRITE)


def refsites(img, lo, hi=None):
    r, _ = text_refs(img, lo, hi)
    return r


# ---------------------------------------------------------------- static checks
def k1(img):
    r = refsites(img, 0x002350C0)
    report("K1a", [(x["site"], x["form"], x["func"]) for x in r] == [(0x00234022, "call", 0x00233F70)],
           "002350C0 callers: %s" % ["%08X %s fn=%08X" % (x["site"], x["form"], x["func"]) for x in r])
    report("K1b", not [d for d in data_refs(img, 0x002350C0) if d[2] == "va64"], "no 8-byte pointer constant names 002350C0")
    r = refsites(img, 0x00233F70)
    report("K1c", [(x["site"], x["text"]) for x in r] == [(0x00265A4F, "lea r13, [rip - 0x31ae6]")]
           and txt(img, 0x00265AA8) == "mov qword ptr [rbx + 0x38], r13",
           "00233F70 is named only at 00265A4F (lea r13) and stored at record +0x38 by 00265AA8")
    want = {0x0025E1AD: "and byte ptr [rdi + 0xd], 0xbf", 0x0025E20E: "mov rax, qword ptr [rdi + 0x38]",
            0x0025E217: "or byte ptr [rdi + 0xd], 0x40", 0x0025E21B: "mov rdx, rdi", 0x0025E222: "call rax",
            0x002672F0: "movzx eax, byte ptr [rcx + 0xd]", 0x002672F4: "shr eax, 6", 0x002672F7: "and eax, 1",
            0x002672FA: "ret",
            0x00233F7D: "mov rdi, rdx", 0x00233F80: "call 0x31b760", 0x00263E30: "mov rax, qword ptr [rcx + 0x30]",
            0x002344EF: "mov qword ptr [rbx + 0x10], rsi", 0x002134A0: "mov qword ptr [rcx + 0x30], rdx",
            0x00233FAD: "test cl, 8", 0x00233FB8: "bt rax, 0x10", 0x00233FC3: "test cl, 0x10",
            0x00233F91: "call 0x2671c0", 0x00233F9E: "call 0x383c80",
            0x0023401E: "mov rcx, qword ptr [rbx + 0x10]", 0x00234022: "call 0x2350c0"}
    bad = ["%08X %r != %r" % (a, txt(img, a), t) for a, t in want.items() if txt(img, a) != t]
    report("K1d", not bad, "drive loop clears +0x0D bit 6 (0025E1AD), sets it (0025E217) and calls record+0x38 (0025E222); "
           "002672F0 returns that bit; the unit is record+0x30 and unit+0x10 is the record (binder 002344EF / 002134A0); "
           "00233F70's gates and its call at 00234022 %s" % bad)


def k2(img):
    want = {0x002350DE: "call 0x2672f0", 0x002350F3: "call 0x31b760", 0x00235104: "cmp byte ptr [rax + 0x50], bpl",
            0x0023511A: "movzx eax, byte ptr [rcx + 5]", 0x00235126: "test byte ptr [rsi], 0x10",
            0x0023513E: "test eax, 0x80000003", 0x00235145: "call 0x313f60",
            0x00235152: "mov rax, qword ptr [rsi + 0x6a0]", 0x00235159: "test byte ptr [rax], 0x10",
            0x00235162: "movzx ecx, byte ptr [rsi + 0x50]", 0x00235173: "sub ecx, 1", 0x00235176: "je 0x2351ee",
            0x00235178: "cmp ecx, 1", 0x0023517B: "jne 0x2351bf",
            0x0023517D: "call 0x3272a0", 0x0023518A: "movzx ecx, byte ptr [rsi + 0x51]", 0x00235193: "call 0x320940",
            0x0023519A: "js 0x2351bf", 0x0023519C: "movss xmm6, dword ptr [rsi + 0x4c]", 0x002351AD: "mulss xmm6, xmm6",
            0x002351A1: "lea rcx, [rbx + 0xe0]", 0x002351B6: "comiss xmm0, xmm6", 0x002351B9: "jbe 0x23529a",
            0x00235200: "call 0x265020", 0x0023520F: "mulss xmm6, xmm6", 0x00235215: "call 0x31b810",
            0x00235222: "test byte ptr [rax], 0x10", 0x00235239: "test ecx, 0x80000003",
            0x0023524D: "call 0x3273b0", 0x0023527D: "comiss xmm6, xmm0", 0x00235280: "ja 0x2351bf",
            0x00235286: "mov ebp, 1", 0x0023528D: "cmp edi, 4", 0x00235292: "test ebp, ebp",
            0x002352A6: "or dword ptr [rcx], 1", 0x002352A9: "mov edx, 1", 0x002352B1: "call 0x300e40",
            0x002352B6: "xor edx, edx", 0x002352BB: "call 0x306e60", 0x002352C0: "mov eax, 1",
            0x003A1960: "movss xmm1, dword ptr [rcx]", 0x003A1964: "movss xmm0, dword ptr [rcx + 8]",
            0x0031E620: "jmp 0x3a1960"}
    bad = ["%08X %r != %r" % (a, txt(img, a), t) for a, t in want.items() if txt(img, a) != t]
    report("K2a", not bad and target(ins(img, 0x00235205)) == RANGE,
           "gate chain, mode split (1 = slot loop on [02089368], 2 = leader vs anchor with unit +0x4C) and action sites %s" % bad)
    r = refsites(img, RANGE, RANGE + 4)
    got = [(x["site"], is_write(img, x["site"])) for x in r]
    report("K2b", got == [(0x00235205, False), (0x0023A1E0, True), (0x0023A540, True)],
           "02089368: read at 00235205 only; written by 0023A1E0 (in 0023A1D0) and 0023A540 (in 0023A520) %s"
           % ["%08X %s" % (a, "W" if w else "r") for a, w in got])
    kva = target(ins(img, 0x0023A538))
    k = struct.unpack("<f", img.read(kva, 4))[0]
    report("K2c", txt(img, 0x0023A538) == "movss xmm0, dword ptr [rip + 0x6da1b4]" and k == 43.0,
           "0023A520 installs 43.0 (constant %08X)" % kva)
    callers = {a: [(x["site"], x["func"]) for x in refsites(img, a)] for a in (0x0023A1D0, 0x0023A520, 0x00238FC0)}
    report("K2d", callers == {0x0023A1D0: [(0x0050F459, 0x0050F410)], 0x0023A520: [(0x00510710, None)],
                              0x00238FC0: [(0x0050F4F5, 0x0050F4A0)]},
           "setters reached only from verb wrappers: %s" % {"%08X" % k_: ["%08X" % s for s, f in v] for k_, v in callers.items()})
    want = {0x00238FCF: "mov ebx, r9d", 0x00238FE1: "mov byte ptr [rax + 0x50], bl", 0x00238FE4: "cmp ebx, 2",
            0x00238FE7: "jne 0x23900f", 0x00239006: "movss dword ptr [rax + 0x4c], xmm0",
            0x0023900B: "mov byte ptr [rax + 0x51], sil"}
    bad = ["%08X %r" % (a, txt(img, a)) for a, t in want.items() if txt(img, a) != t]
    report("K2e", not bad, "00238FC0 stores the mode always and the threshold/anchor only for mode 2 %s" % bad)


def edx_before(img, site):
    pd, fn = decode_fn(img, site)
    if fn is None:
        return "?"
    addrs = sorted(a for a in fn if a < site)
    for a in reversed(addrs[-8:]):
        t = (fn[a].mnemonic + " " + fn[a].op_str)
        if t.startswith(("mov edx,", "xor edx, edx", "mov dl,", "lea edx,", "mov rdx,", "movzx edx,", "sete dl",
                         "setne dl")):
            return t
        if fn[a].mnemonic in ("call",) or fn[a].mnemonic.startswith("j"):
            return "unset-before-" + t
    return "?"


def k3(img):
    want = {0x00300E4F: "mov ebx, edx", 0x00300EE4: "je 0x300f5d", 0x00300EEC: "jne 0x300f5d",
            0x00300F5D: "test ebx, ebx", 0x00300F5F: "jne 0x300f6d", 0x00300F68: "call 0x237080",
            0x00237085: "and dword ptr [rcx], 0xffffff7a"}
    bad = ["%08X %r" % (a, txt(img, a)) for a, t in want.items() if txt(img, a) != t]
    # rbx is not rewritten between 00300E4F and the spawn-backed exit 00300F5D on the path through 00300EEC
    body = list(img.cs.disasm(img.read(0x00300E54, 0x00300EF0 - 0x00300E54), 0x00300E54))
    clob = [c.address for c in body if c.op_str.startswith(("ebx", "rbx", "bl")) and c.mnemonic not in ("cmp", "test")]
    report("K3a", not bad and not clob, "teardown 00300E40: arg2 held in ebx from 00300E4F (no rewrite before 00300EEC %s); "
           "spawn-backed tail calls the record clear 00237080 (0xFFFFFF7A: bits 0, 2, 7) only when arg2 == 0 %s" % (clob, bad))
    rows = [(x["site"], x["func"], edx_before(img, x["site"])) for x in refsites(img, 0x00300E40)]
    for s, f, e in rows:
        note("teardown call %08X fn=%08X  %s" % (s, f or 0, e))
    ones = [s for s, f, e in rows if e == "mov edx, 1"]
    zeros = [s for s, f, e in rows if e == "xor edx, edx"]
    report("K3b", len(rows) == 10 and ones == [0x002352B1] and len(zeros) == 9,
           "ten teardown call sites: the retire alone passes 1 (002352A9); the other nine pass 0 (xor edx, edx), so "
           "every other teardown of a spawn-backed unit clears record bits 0/2/7; constant-1 callers: %s"
           % ["%08X" % s for s in ones])
    want = {0x002358B6: "mov eax, dword ptr [r14]", 0x002358B9: "test al, 1", 0x002358BB: "jne 0x2358dd",
            0x002358BD: "test al, 2", 0x002358D7: "jb 0x2359c4", 0x002358A1: "movzx eax, word ptr [r14 + 0xa]",
            0x002358B0: "jae 0x2359c4"}
    bad = ["%08X %r" % (a, txt(img, a)) for a, t in want.items() if txt(img, a) != t]
    report("K3c", not bad, "the automatic selector tests the death limit (002358A1-002358B0), then admits a bit-0 entry "
           "past the cooldown (002358B9/002358BB) %s" % bad)
    r = refsites(img, 0x00236670)
    report("K3d", [(x["site"], x["func"]) for x in r] == [(0x0050FC9C, 0x0050FC90)],
           "SpawnEntry_QueryRangeReentryPending 00236670 has one caller, verb wrapper 0050FC90 (%s)"
           % ["%08X" % x["site"] for x in r])


def k4(img):
    r = refsites(img, WINDOW, WINDOW + 4)
    got = [(x["site"], is_write(img, x["site"])) for x in r]
    report("K4a", got == [(0x002337FA, False), (0x00235330, False), (0x0023534A, True), (0x00236A0D, True)],
           "0208936C: readers 002337FA, 00235330; writers 0023534A, 00236A0D %s" % ["%08X %s" % (a, "W" if w else "r") for a, w in got])
    report("K4b", txt(img, 0x00236A0D) == "mov dword ptr [rip + 0x1e52955], 0x12c" and
           [x["site"] for x in refsites(img, 0x002368D0)] == [0x0022A41A],
           "00236A0D stores 300 inside 002368D0, whose one caller is 0022A41A")
    want = {0x00235340: "test ecx, ecx", 0x00235342: "mov eax, 0x12c", 0x00235347: "cmovs ecx, eax"}
    bad = ["%08X %r" % (a, txt(img, a)) for a, t in want.items() if txt(img, a) != t]
    g = [(x["site"], x["func"]) for x in refsites(img, 0x00235330)]
    s = [(x["site"], x["func"]) for x in refsites(img, 0x00235340)]
    report("K4c", not bad and g == [(0x00510819, 0x00510810)] and s == [(0x00510802, 0x005107F0)],
           "getter 00235330 <- 00510819 (wrapper 00510810) only; setter 00235340 <- 00510802 (wrapper 005107F0) only %s" % bad)
    report("K4d", not data_refs(img, WINDOW, WINDOW + 4), "no .rdata/.data pointer constant names 0208936C")


def k5(img):
    r = refsites(img, 0x00233780)
    report("K5a", [(x["site"], x["func"]) for x in r] == [(0x00234423, 0x002343CD)] and
           not [d for d in data_refs(img, 0x00233780) if d[2] == "va64"],
           "00233780: one caller 00234423 (chained body 002343CD of 002342F0), no pointer constant")
    want = {0x002342F4: "cmp dword ptr [rip + 0x1e55005], 0", 0x002342FB: "je 0x234471",
            0x00234349: "call 0x239960", 0x002343CB: "je 0x234423", 0x0023441E: "call 0x3924b0",
            0x00234423: "call 0x233780"}
    bad = ["%08X %r" % (a, txt(img, a)) for a, t in want.items() if txt(img, a) != t]
    report("K5b", not bad and img.pdata(0x002343CD)[0] == 0x002343CD,
           "002342F0 skips everything when [02089300] == 0 (002342F4), else calls the -2 reset route 00239960 "
           "(00234349) and reaches the rotation on both arms of 002343CB %s" % bad)
    report("K5c", [x["site"] for x in refsites(img, 0x002342F0)] == [0x00267136, 0x0026CEC6],
           "002342F0 callers 00267136, 0026CEC6")
    r = refsites(img, LAST, LAST + 6)
    got = [(x["site"], is_write(img, x["site"]), target(ins(img, x["site"]))) for x in r]
    for a, w, t in got:
        note("%08X %s %08X  %s" % (a, "W" if w else "r", t or 0, txt(img, a)))
    writers = sorted((a, t) for a, w, t in got if w)
    report("K5d", writers == [(0x002335BC, PREV), (0x002335C7, LAST), (0x002339F4, LAST), (0x00233A03, STAMP),
                              (0x00233A11, PREV), (0x00237E53, STAMP), (0x00237E5D, PREV), (0x00237E64, LAST)],
           "history/stamp writers: the rotation tail, the reset 00237DF0 and the restore 00233550 (field words only)")
    readers = sorted((a, t) for a, w, t in got if not w)
    report("K5e", readers == [(0x00233529, PREV), (0x00233533, LAST), (0x002337CD, PREV), (0x002337F0, STAMP),
                              (0x002339E5, LAST)],
           "readers: serializer 00233529/00233533 (field words only), the rotation's compare 002337CD (previous), "
           "its window 002337F0 (stamp) and its shift 002339E5 (last)")
    want = {0x002337C1: "call 0x3148f0", 0x003148FB: "mov eax, dword ptr [rax + 0x1044]", 0x00314903: "cmovs eax, ecx",
            0x002337CD: "movsx ecx, word ptr [rip + 0x1e55b9e]", 0x002337D6: "cmp esi, ecx", 0x002337D8: "jne 0x23393f",
            0x00233801: "cmp ecx, edx", 0x00233803: "ja 0x23393f", 0x0023378D: "cmp qword ptr [rip + 0x1e5aefb], 0",
            0x00233795: "je 0x233a18", 0x002337A3: "je 0x233a18", 0x00233A18: "add rsp, 0x9428"}
    bad = ["%08X %r" % (a, txt(img, a)) for a, t in want.items() if txt(img, a) != t]
    report("K5f", not bad and target(ins(img, 0x0023378D)) == BANK1 and target(ins(img, 0x0023379B)) == BANK2,
           "rotation: null bank -> 00233A18 (no shift, no stamp); field id clamped >= 0 (00314903); "
           "signed-extended previous word compared (002337CD); unsigned window `ja` (00233803) %s" % bad)


# ---------------------------------------------------------------- Unicorn harness
STACK, STACK_SZ = 0x70000000, 0x100000
HEAP, HEAP_SZ = 0x80000000, 0x200000
SENT = 0x60000000


class Emu(object):
    def __init__(self, img):
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        size = (0x2F76000 + 0xFFF) & ~0xFFF
        uc.mem_map(img.base, size)
        for name, va, vs, ra, rs in img.secs:
            n = min(vs, rs)
            uc.mem_write(img.base + va, img.d[ra:ra + n])
        uc.mem_map(STACK, STACK_SZ)
        uc.mem_map(HEAP, HEAP_SZ)
        uc.mem_map(SENT, 0x1000)
        uc.mem_write(SENT, b"\xF4")
        self.uc = uc
        self.log = []

    def stub(self, addr, fn):
        def cb(uc, a, sz, ud):
            r = fn(uc)
            if r is not None:
                uc.reg_write(UC_X86_REG_RAX, r & 0xFFFFFFFFFFFFFFFF)
            sp = uc.reg_read(UC_X86_REG_RSP)
            ret = struct.unpack("<Q", uc.mem_read(sp, 8))[0]
            uc.reg_write(UC_X86_REG_RSP, sp + 8)
            uc.reg_write(UC_X86_REG_RIP, ret)
        self.uc.hook_add(UC_HOOK_CODE, cb, None, addr, addr)

    def w(self, a, fmt, *v):
        self.uc.mem_write(a, struct.pack(fmt, *v))

    def r(self, a, fmt):
        return struct.unpack(fmt, bytes(self.uc.mem_read(a, struct.calcsize(fmt))))

    def call(self, entry, rcx=0, rdx=0, limit=5000000):
        sp = STACK + STACK_SZ - 0x1000
        self.w(sp, "<Q", SENT)
        self.uc.reg_write(UC_X86_REG_RSP, sp)
        self.uc.reg_write(UC_X86_REG_RCX, rcx)
        self.uc.reg_write(UC_X86_REG_RDX, rdx)
        self.uc.emu_start(entry, SENT, count=limit)
        return self.uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


def run_rotation(img, field, prev, last, stamp, ticks, window, scale=1.0, nullbank=False):
    e = Emu(img)
    B1, B2 = HEAP + 0x1000, HEAP + 0x20000
    p1 = bytes(((i * 7 + 1) & 0xFF) for i in range(0x9400))
    p2 = bytes(((i * 13 + 5) & 0xFF) for i in range(0x9400))
    e.uc.mem_write(B1, p1)
    e.uc.mem_write(B2, p2)
    e.w(BANK1, "<Q", 0 if nullbank else B1)
    e.w(BANK2, "<Q", B2)
    e.w(LAST, "<h", last)
    e.w(PREV, "<h", prev)
    e.w(STAMP, "<I", stamp & 0xFFFFFFFF)
    e.w(TICKS, "<I", ticks & 0xFFFFFFFF)
    e.w(WINDOW, "<i", window)
    e.w(SCALE, "<f", scale)
    e.uc.mem_write(COUNTERS, b"\x5A\x5A" * 0x80)
    e.w(PARITY, "<B", 0)
    e.stub(0x003148F0, lambda uc: field)
    e.stub(0x00808F10, lambda uc: None)            # __chkstk: probes only, rax kept

    def memset(uc):
        d = uc.reg_read(UC_X86_REG_RCX)
        v = uc.reg_read(UC_X86_REG_RDX) & 0xFF
        n = uc.reg_read(UC_X86_REG_R8)
        uc.mem_write(d, bytes([v]) * n)
        e.log.append(("memset", d, v, n))
        return d
    e.stub(0x00861EC0, memset)
    e.call(0x00233780)
    out = {
        "b1ptr": e.r(BANK1, "<Q")[0], "b2ptr": e.r(BANK2, "<Q")[0],
        "b1": bytes(e.uc.mem_read(B1, 0x9400)), "b2": bytes(e.uc.mem_read(B2, 0x9400)),
        "last": e.r(LAST, "<h")[0], "prev": e.r(PREV, "<h")[0], "stamp": e.r(STAMP, "<I")[0],
        "parity": e.r(PARITY, "<B")[0],
        "c0": e.r(COUNTERS, "<64H"), "c1": e.r(COUNTERS + 0x80, "<64H"), "log": e.log,
    }
    out["restored"] = out["b1"] == p2 and out["b2"] == p1
    out["wiped"] = out["b1"] == b"\0" * 0x9400 and out["b2"] == p1
    out["untouched"] = out["b1"] == p1 and out["b2"] == p2
    out["B1"], out["B2"] = B1, B2
    return out


def k6(img, tag_prefix="K6"):
    ok_all = {}
    A, B = 12, 34
    # a: A -> B -> A within the window
    o = run_rotation(img, field=A, prev=A, last=B, stamp=1000, ticks=1000 + 4500, window=300)
    ok_all["a"] = report(tag_prefix + "a", o["restored"] and o["b1ptr"] == o["B1"] and o["b2ptr"] == o["B2"] and o["parity"] == 1
                         and o["c0"] == (0x5A5A,) * 64 and o["c1"] == (0x5A5A,) * 64 and not o["log"]
                         and (o["prev"], o["last"], o["stamp"]) == (B, A, 5500),
                         "A->B->A after 150 s of a 300 s window: contents exchanged, pointers kept, parity 1, counters "
                         "untouched, no memset; history (prev, last) = (%d, %d), stamp %d" % (o["prev"], o["last"], o["stamp"]))
    # b: boundary
    o1 = run_rotation(img, field=A, prev=A, last=B, stamp=1000, ticks=1000 + 9000, window=300)
    o2 = run_rotation(img, field=A, prev=A, last=B, stamp=1000, ticks=1000 + 9001, window=300)
    ok_all["b"] = report(tag_prefix + "b", o1["restored"] and o2["wiped"],
                         "elapsed 9000 ticks (= 30 x 1.0 x 300) restores; 9001 wipes")
    # c: different field
    o = run_rotation(img, field=56, prev=A, last=B, stamp=1000, ticks=1100, window=300)
    ok_all["c"] = report(tag_prefix + "c", o["wiped"] and o["parity"] == 1 and o["c1"] == (1,) * 64
                         and o["c0"] == (0x5A5A,) * 64 and o["log"] == [("memset", o["B1"], 0, 0x9400)]
                         and (o["prev"], o["last"]) == (B, 56),
                         "a third field wipes: bank 2 <- bank 1, bank 1 zeroed (one memset 0x9400), parity 0 -> 1, the 64 "
                         "counters at 0208D3D4 = 1, the 64 at 0208D354 untouched")
    # d: stamp later than the clock
    o = run_rotation(img, field=A, prev=A, last=B, stamp=5000, ticks=4000, window=300)
    ok_all["d"] = report(tag_prefix + "d", o["wiped"], "stamp 5000 > clock 4000: the unsigned difference FFFFFC18 wipes")
    # e: after the reset's -1 history
    hits = [f for f in (0, 1, 0x7FFF) if run_rotation(img, field=f, prev=-1, last=-1, stamp=0, ticks=10, window=300)["restored"]]
    ok_all["e"] = report(tag_prefix + "e", not hits, "previous = -1 (the reset's value): fields 0, 1, 0x7FFF all wipe %s" % hits)
    # f: null bank
    o = run_rotation(img, field=A, prev=A, last=B, stamp=1000, ticks=2000, window=300, nullbank=True)
    ok_all["f"] = report(tag_prefix + "f", (o["prev"], o["last"], o["stamp"], o["parity"]) == (A, B, 1000, 0) and not o["log"],
                         "bank 1 null: returns with history, stamp and parity unchanged")
    # g: scale 2.0
    o1 = run_rotation(img, field=A, prev=A, last=B, stamp=0, ticks=18000, window=300, scale=2.0)
    o2 = run_rotation(img, field=A, prev=A, last=B, stamp=0, ticks=18001, window=300, scale=2.0)
    ok_all["g"] = report(tag_prefix + "g", o1["restored"] and o2["wiped"], "scale 2.0: 18000 ticks restores, 18001 wipes")
    # h: returning to the field you just left (A -> A) wipes unless previous is also A
    o = run_rotation(img, field=B, prev=A, last=B, stamp=0, ticks=10, window=300)
    ok_all["h"] = report(tag_prefix + "h", o["wiped"], "field == last (B) with previous A: wipes")
    return ok_all


def run_retire(img, mode=1, rng=43.0, me=(0.0, 0.0), slots=None, focus=0x1234, unit_flags=0x10, optin=True, spawn_backed=1,
               status=0, waiver=1, inhibit=False, thr=6.0, anchor=(0.0, 0.0), anchor_ok=True, leader=(0.0, 0.0),
               have_leader=True):
    """slots: list of 4 entries (None or (x, z, flags, handle)); positions are XZ."""
    e = Emu(img)
    H = HEAP
    A, U, BK, R, L = H + 0x100, H + 0x1000, H + 0x3000, H + 0x4000, H + 0x5000
    SL = [H + 0x8000 + i * 0x1000 for i in range(4)]
    SA = [H + 0x10000 + i * 0x100 for i in range(4)]
    SB = [H + 0x14000 + i * 0x100 for i in range(4)]
    e.w(A + 0x0D, "<B", 0x40 if optin else 0)
    e.w(A + 0x30, "<Q", U)
    e.w(U, "<Q", unit_flags)
    e.w(U + 0x10, "<Q", A)
    e.w(U + 0x4C, "<f", thr)
    e.w(U + 0x50, "<B", mode)
    e.w(U + 0x51, "<B", 7)
    e.w(U + 0x698, "<Q", BK)
    e.w(U + 0x6A0, "<Q", R)
    e.w(BK + 5, "<B", spawn_backed)
    e.w(BK + 0x3C, "<I", status)
    e.w(BK + 0x64, "<I", 0)
    e.w(R, "<I", 0x02 | (0x10 if inhibit else 0))
    e.w(L + 0xE0, "<f", leader[0])
    e.w(L + 0xE8, "<f", leader[1])
    e.w(RANGE, "<f", rng)
    pos = {A: me}
    slots = list(slots or []) + [None] * (4 - len(slots or []))
    for i, s in enumerate(slots):
        if s is None:
            continue
        x, z, fl, h = s
        e.w(SL[i], "<I", fl)
        e.w(SL[i] + 8, "<I", h)
        e.w(SL[i] + 0x10, "<Q", SA[i])
        e.w(SL[i] + 0x698, "<Q", SB[i])
        pos[SA[i]] = (x, z)
    e.stub(0x00808C40, lambda uc: None)
    e.stub(0x00313F60, lambda uc: waiver)
    e.stub(0x003272A0, lambda uc: (L if have_leader else 0))

    def fetch(uc):
        e.log.append(("anchor", uc.reg_read(UC_X86_REG_RCX) & 0xFF))
        if not anchor_ok:
            return 0xFFFFFFFF
        out = uc.reg_read(UC_X86_REG_RDX)
        uc.mem_write(out, struct.pack("<fff", anchor[0], 0.0, anchor[1]))
        return 0
    e.stub(0x00320940, fetch)

    def getpos(uc):
        a = uc.reg_read(UC_X86_REG_RCX)
        x, z = pos.get(a, (float("nan"), float("nan")))
        uc.mem_write(uc.reg_read(UC_X86_REG_RDX), struct.pack("<f", x))
        uc.mem_write(uc.reg_read(UC_X86_REG_R8), struct.pack("<f", 0.0))
        uc.mem_write(uc.reg_read(UC_X86_REG_R9), struct.pack("<f", z))
        return None
    e.stub(0x00265020, getpos)
    e.stub(0x0031B810, lambda uc: (SL[uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF] if slots[uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF] else 0))
    e.stub(0x003273B0, lambda uc: 1 if (uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF) == focus else 0)

    def teardown(uc):
        e.log.append(("teardown", uc.reg_read(UC_X86_REG_RCX), uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF,
                      e.r(R, "<I")[0]))
        return None
    e.stub(0x00300E40, teardown)
    e.stub(0x00306E60, lambda uc: e.log.append(("unregister", uc.reg_read(UC_X86_REG_RCX),
                                                uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF)) or None)
    ret = e.call(0x002350C0, rcx=A)
    return {"ret": ret, "log": [x for x in e.log if x[0] != "anchor"], "anchor": [x for x in e.log if x[0] == "anchor"],
            "rec": e.r(R, "<I")[0], "U": U}


FOCUS = 0x1234


def slot(x, z, h=FOCUS, fl=0x10):
    return (x, z, fl, h)


def retired(o):
    return o["ret"] == 1 and [x[0] for x in o["log"]] == ["teardown", "unregister"]


def kept(o):
    return o["ret"] == 0 and not o["log"]


def k7(img, tp="K7"):
    res = {}
    a0 = run_retire(img, mode=0, slots=[slot(100.0, 0.0)])
    a3 = run_retire(img, mode=3, slots=[slot(100.0, 0.0)])
    res["a"] = report(tp + "a", kept(a0) and kept(a3), "mode 0 and mode 3: return 0, no call")
    near = run_retire(img, mode=1, slots=[slot(10.0, 0.0)])
    far = run_retire(img, mode=1, slots=[slot(50.0, 0.0)])
    eq = run_retire(img, mode=1, slots=[slot(43.0, 0.0)])
    res["b"] = report(tp + "b", kept(near) and retired(far) and retired(eq),
                      "mode 1, range 43: focus at 10 kept, at 50 retired, at exactly 43 retired (`ja` keeps only when nearer)")
    z = run_retire(img, mode=1, rng=0.0, slots=[slot(0.5, 0.0)])
    res["c"] = report(tp + "c", retired(z), "mode 1 with the range unset (0.0): focus at 0.5 retired")
    nf = run_retire(img, mode=1, slots=[slot(1.0, 0.0, h=0x99), slot(50.0, 0.0)])
    none = run_retire(img, mode=1, slots=[slot(50.0, 0.0, h=0x99), None, slot(60.0, 0.0, fl=0)])
    res["d"] = report(tp + "d", retired(nf) and kept(none),
                      "mode 1 ignores a near non-focus slot (retired); no eligible focus slot keeps the unit")
    m2in = run_retire(img, mode=2, leader=(5.0, 0.0))
    m2eq = run_retire(img, mode=2, leader=(6.0, 0.0))
    m2out = run_retire(img, mode=2, leader=(7.0, 0.0))
    res["e"] = report(tp + "e", retired(m2in) and retired(m2eq) and kept(m2out) and m2in["anchor"] == [("anchor", 7)],
                      "mode 2, threshold 6: leader at 5 and 6 retires (`jbe`), at 7 kept; anchor index from unit +0x51")
    nofetch = run_retire(img, mode=2, leader=(1.0, 0.0), anchor_ok=False)
    nolead = run_retire(img, mode=2, leader=(1.0, 0.0), have_leader=False)
    res["f"] = report(tp + "f", kept(nofetch) and kept(nolead), "mode 2: failed anchor fetch or no leader keeps the unit")
    g = [kept(run_retire(img, mode=1, slots=[slot(50.0, 0.0)], inhibit=True)),
         kept(run_retire(img, mode=1, slots=[slot(50.0, 0.0)], optin=False)),
         kept(run_retire(img, mode=1, slots=[slot(50.0, 0.0)], spawn_backed=0)),
         kept(run_retire(img, mode=1, slots=[slot(50.0, 0.0)], status=1, waiver=0)),
         retired(run_retire(img, mode=1, slots=[slot(50.0, 0.0)], status=1, waiver=1)),
         kept(run_retire(img, mode=1, slots=[slot(50.0, 0.0)], unit_flags=0))]
    res["g"] = report(tp + "g", all(g), "inhibit bit 4 / opt-in clear / bkbi[5]==0 / status without waiver / unit bit 4 "
                      "clear keep; status with waiver retires %s" % g)
    o = far
    lg = o["log"]
    res["h"] = report(tp + "h", o["ret"] == 1 and len(lg) == 2 and lg[0][1] == o["U"] and lg[0][2] == 1 and (lg[0][3] & 1) == 1
                      and lg[1] == ("unregister", o["U"], 0) and (o["rec"] & 1) == 1,
                      "action: record bit 0 already set at teardown(unit, %s), then unregister(unit, 0); returns 1; record "
                      "flags %08X" % (lg[0][2] if lg else None, o["rec"]))
    n1 = run_retire(img, mode=1, slots=[slot(float("nan"), 0.0)])
    n2 = run_retire(img, mode=2, leader=(float("nan"), 0.0))
    res["i"] = report(tp + "i", retired(n1) and retired(n2), "an unordered (NaN) distance retires in mode 1 and in mode 2")
    return res, z


def main():
    print("FABLE check_s16 - S-16 range retirement, the return window and the keep-bank rotation (2026-10-03)")
    print("unicorn %s" % UC_VERSION)
    img = Img.load()
    print("image sha256 verified (rvlib), base %08X" % img.base)
    report("V0", UC_VERSION == "2.1.4", "unicorn pinned 2.1.4")
    k1(img)
    k2(img)
    k3(img)
    k4(img)
    k5(img)
    k6(img)
    k7res, zrun = k7(img)

    # ---------------- sensitivity controls
    quiet[0] = True
    saved = fails

    def under(patch_va, patch_bytes, fn):
        global fails
        f0 = fails
        pimg = img.patched(patch_va, patch_bytes)
        out = fn(pimg)
        d = fails - f0
        fails = f0
        return out, d

    # S1: ja (0F 87) -> jg (0F 8F) at 00233803
    out, _ = under(0x00233803, b"\x0F\x8F", lambda p: k6(p, "s1."))
    s1 = not out["d"]
    # S2: 002337CD movsx ecx, word [rip+disp]: disp - 2 makes it read 02089370
    disp = struct.unpack("<i", img.read(0x002337D0, 4))[0]
    out2, _ = under(0x002337D0, struct.pack("<i", disp - 2), lambda p: k6(p, "s2."))
    s2 = not out2["a"]
    # S3: jbe (0F 86) -> ja (0F 87) at 002351B9
    out3, _ = under(0x002351B9, b"\x0F\x87", lambda p: k7(p, "s3.")[0])
    s3 = not out3["e"]
    # S4: mov edx, 1 -> mov edx, 0 at 002352A9 (BA 01 00 00 00)
    out4, _ = under(0x002352A9, b"\xBA\x00\x00\x00\x00", lambda p: k7(p, "s4.")[0])
    s4 = not out4["h"]
    quiet[0] = False
    assert fails == saved
    report("S1", s1, "00233803 ja -> jg (signed window): K6d fails, so K6d measures the unsigned compare")
    report("S2", s2, "002337CD reads 02089370 (last) instead of 02089372 (previous): K6a fails")
    report("S3", s3, "002351B9 jbe -> ja (mode 2 sense inverted): K7e fails")
    report("S4", s4, "002352A9 edx 1 -> 0: K7h fails, so K7h measures the teardown's second argument")
    claim = not retired(zrun)        # the mutated claim "an unset range never retires a unit 0.5 away"
    report("S5", not claim, "the mutated claim 'an unset range (0.0) never retires a unit 0.5 from the focus member' is "
           "refuted by the execution (K7c retired it)")
    print("FAILS %d" % fails)
    return fails


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
