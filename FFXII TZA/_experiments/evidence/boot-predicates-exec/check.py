# boot-fixups section 13c predicate layer — runtime validation for
# CONTRACT-boot-fixups.md. Executes on shipped bytes under Unicorn:
#
#   001EDDA0 (27 B): predicate — cmp d[01DFE0C0] (suppressor) first,
#     then d[01F82E38] (mode flag); returns 0 iff flag set AND
#     unsuppressed, else 1.
#   001EDEC0 (40 B): predicate — cmp d[01F82E38] FIRST (order differs
#     from DA0), then d[01DFE0C0]; returns 1 unless flag set AND
#     unsuppressed, then returns (~ecx) & 1.
#   001EDE70 (7 B): returns d[01F82E38] verbatim.
#   001EDE80 (61 B): flag then suppressor; returns 1 unless flag set
#     AND unsuppressed, then returns 0022A080() + 0022A030()
#     (both real leaves: d[02064AD8] + d[02064AA8]).
#   001EDEF0 (7 B): d[01DFE0C0] = ecx verbatim (no bool normalisation).
#   00184960 (123 B): suppressor gate — EF0(1) on entry; flag==0 ->
#     tail (suppressor stays 1); mode(ecx)!=1 -> EF0(0), ebx=1;
#     mode==1: gate d[02092748]!=0 -> require 00229EA0() (movsx of
#     b[02064AD3]) == mode else EF0(0) bypassing the byte check;
#     then b[001EBA40()+0x118]==0 -> tail (stays 1), else EF0(0).
#     Tail: 00798E90(ebx) clamp-store [1,3] -> d[01F3DA18];
#     00189120() -> q[0207F598]; nonzero -> tail jmp 005FEA50 with
#     rcx=q[rax+8], rdx=001844B0, r8=ebx.
#   001EBA40: singleton getter — q[02022E18] or lazy-init via
#     00210EC0(0x2E0) + 001EB190.
#   0022BDF0 (143 B): frame-base selector — ebp = (0017D8F0()==1)
#     (real leaf: d[q[01F82D20]+0x48], settings row 18); argv loop
#     compares the first 8 bytes of each argument against "-nologo\0"
#     at 00908BD8 and calls 00314DE0(1) (real: d[022C2528]=ecx) on
#     exact match; tail-jmps 001EDDC0 with ecx=ebp.
#
#   Scripted boundaries (entry-intercepted, disclosed): 001EDDC0
#   (EXP-142's scope — ecx recorded, not re-run), 005FEA50 (registry
#   vtable dispatch — args recorded), 00210EC0 allocator (planted
#   heap pointer), 001EB190 singleton init (intercepted). Everything
#   else executes as shipped bytes.
#
import hashlib
import json
import os
import struct
import sys

from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x30A0000
HEAP = 0x40000000
STACK = 0x61000000
RETQ = 0x62000000

# ---- subjects (all executed as shipped bytes) ----
P_DA0   = 0x001EDDA0       # predicate: 0 iff flag && !supp
P_EC0   = 0x001EDEC0       # predicate: 1 unless on -> (~ecx)&1
P_E70   = 0x001EDE70       # returns flag
P_E80   = 0x001EDE80       # 1 unless on -> 22A080()+22A030()
W_EF0   = 0x001EDEF0       # suppressor writer
G_4960  = 0x00184960       # suppressor gate
S_EBA40 = 0x001EBA40       # singleton getter
S_A080  = 0x0022A080       # leaf: d[02064AD8]
S_A030  = 0x0022A030       # leaf: d[02064AA8]
S_9EA0  = 0x00229EA0       # leaf: movsx b[02064AD3]
S_8F0   = 0x0017D8F0       # leaf: settings row 18
S_4DE0  = 0x00314DE0       # leaf: d[022C2528]=ecx
S_98E90 = 0x00798E90       # leaf: clamp [1,3] -> d[01F3DA18]
S_9120  = 0x00189120       # leaf: q[0207F598]
S_BDF0  = 0x0022BDF0       # frame-base selector + -nologo scan

# ---- scripted boundaries ----
X_DDC0  = 0x001EDDC0       # 22BDF0 tail target (EXP-142's scope)
X_EA50  = 0x005FEA50       # registry vtable dispatch
X_10EC0 = 0x00210EC0       # allocator
X_B190  = 0x001EB190       # singleton init

# ---- globals ----
FLAG    = 0x01F82E38       # mode flag (written only by 001EDDC0)
SUPP    = 0x01DFE0C0       # suppressor (written only by 001EDEF0)
C_4AD8  = 0x02064AD8       # 22A080's cell
C_4AA8  = 0x02064AA8       # 22A030's cell
C_4AD3  = 0x02064AD3       # 229EA0's byte cell
GATE9   = 0x02092748       # 184960's 229EA0-gate cell
SINGLE  = 0x01F82E18       # 1EBA40's singleton cell
SETPTR  = 0x01F82D20       # 17D8F0's settings-block pointer
NOLOGO  = 0x022C2528       # 314DE0's store target
CLAMP   = 0x01F3DA18       # 798E90's clamped store target
REGCELL = 0x01F7F598       # 189120's cell
RDXARG  = 0x0017ECB0       # 184960's lea constant for 5FEA50

RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")


def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)


def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs


class GuestMem:
    def __init__(self, uc, raw, secs):
        self.uc, self.secs = uc, secs
        self.writes, self.ovl = {}, {}
        for va, vs, ra, rs in secs:
            lo = (va + IMG_LO) & ~0xFFF
            hi = (va + IMG_LO + max(vs, rs) + 0xFFF) & ~0xFFF
            uc.mem_map(lo, hi - lo)
            if rs:
                uc.mem_write(va + IMG_LO, raw[ra:ra + rs])

    def w(self, addr, data):
        if isinstance(data, int):
            data = qw(data)
        try:
            self.uc.mem_write(addr, bytes(data))
        except UcError:
            lo = addr & ~0xFFF
            self.uc.mem_map(lo, 0x1000)
            self.uc.mem_write(addr, bytes(data))

    def q(self, a):
        return struct.unpack("<Q", bytes(self.uc.mem_read(a, 8)))[0]

    def d(self, a):
        return struct.unpack("<I", bytes(self.uc.mem_read(a, 4)))[0]

    def b(self, a):
        return self.uc.mem_read(a, 1)[0]


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc, raw, secs)
        self.gm.map = self.uc.mem_map
        self.gm.map(STACK, 0x100000)
        self.gm.map(RETQ, 0x1000)
        self.gm.map(HEAP, 0x200000)
        self.trace, self.faults = [], []
        self.rets = {}

        # ---- fixture ----
        self.gm.w(FLAG, dw(case.get("flag", 0)))
        self.gm.w(SUPP, dw(case.get("supp", 0)))
        self.gm.w(C_4AD8, dw(case.get("c4ad8", 0)))
        self.gm.w(C_4AA8, dw(case.get("c4aa8", 0)))
        self.gm.w(C_4AD3, bytes([case.get("c4ad3", 0) & 0xFF]))
        self.gm.w(GATE9, dw(case.get("gate9", 0)))
        self.gm.w(NOLOGO, dw(0))
        self.gm.w(CLAMP, dw(0))
        self.gm.w(REGCELL, qw(case.get("regcell", 0)))
        # settings block: q[SETPTR] -> heap; row 18 at +0x48
        self.setblk = HEAP + 0x2000
        self.gm.w(SETPTR, qw(case.get("setptr", self.setblk)))
        self.gm.w(self.setblk + 0x48, dw(case.get("row18", 0)))
        # singleton object: byte at +0x118 is the gate byte
        self.singl = HEAP + 0x4000
        if case.get("singleton", 1):
            self.gm.w(SINGLE, qw(self.singl))
            self.gm.w(self.singl + 0x118,
                      bytes([case.get("byte118", 0) & 0xFF]))
        else:
            self.gm.w(SINGLE, qw(0))
        # registry object for 189120 -> 5FEA50 tail
        if case.get("regobj"):
            self.regobj = HEAP + 0x6000
            self.gm.w(REGCELL, qw(self.regobj))
            self.gm.w(self.regobj + 8, qw(HEAP + 0x7000))  # q[rax+8]
        # argv array for 22BDF0 cases
        argv = case.get("argv")
        if argv is not None:
            base = HEAP + 0x8000
            strs = HEAP + 0x9000
            for i, s in enumerate(argv):
                sa = strs + i * 0x40
                self.gm.w(sa, s.encode() + b"\0")
                self.gm.w(base + i * 8, qw(sa))
            self.argv_addr = base

        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def _ret(self):
        rsp = self.uc.reg_read(UC_X86_REG_RSP)
        self.uc.reg_write(UC_X86_REG_RIP, self.gm.q(rsp))
        self.uc.reg_write(UC_X86_REG_RSP, rsp + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("mem", access, addr,
                            uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()
        return False

    MARK = {W_EF0: "ef0", P_E70: "e70", S_A080: "a080",
            S_A030: "a030", S_9EA0: "a9ea0", S_EBA40: "eba40",
            S_8F0: "8f0", S_4DE0: "4de0", S_98E90: "98e90",
            S_9120: "9120"}

    def on_code(self, uc, addr, size, _):
        tag = self.MARK.get(addr)
        if tag is not None:
            self.trace.append(tag)
        if addr == S_98E90:
            self.rets["98e90_ecx"] = uc.reg_read(UC_X86_REG_RCX)
        elif addr == X_DDC0:
            # 22BDF0's tail target: record the selected frame base
            self.trace.append("ddc0")
            self.rets["ddc0_ecx"] = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
            self._ret()
        elif addr == X_EA50:
            self.trace.append("xea50")
            self.rets["ea50_rcx"] = uc.reg_read(UC_X86_REG_RCX)
            self.rets["ea50_rdx"] = uc.reg_read(UC_X86_REG_RDX)
            self.rets["ea50_r8"] = uc.reg_read(UC_X86_REG_R8)
            self._ret()
        elif addr == X_10EC0:
            self.trace.append("x10ec0")
            self.rets["alloc_sz"] = uc.reg_read(UC_X86_REG_RCX)
            self.uc.reg_write(UC_X86_REG_RAX, HEAP + 0xA000)
            self._ret()
        elif addr == X_B190:
            self.trace.append("xb190")
            self.rets["b190_rcx"] = uc.reg_read(UC_X86_REG_RCX)
            self._ret()

    def run(self, entry, rcx=0, rdx=0, r8=0, r9=0):
        uc = self.uc
        rsp = STACK + 0x80000
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RDX, rdx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R8, r8 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R9, r9 & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(entry, RETQ, timeout=120_000_000)
        except UcError as e:
            self.faults.append(("uc", str(e),
                                uc.reg_read(UC_X86_REG_RIP)))
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    out = {"trace": w.trace, "faults": w.faults}
    if name.startswith("da0") or name in ("mut-flag-neg",
                                          "mut-supp-neg"):
        out["ret"] = w.run(P_DA0)
    elif name.startswith("ec0"):
        out["ret"] = w.run(P_EC0, rcx=case.get("arg", 0))
    elif name.startswith("e70"):
        out["ret"] = w.run(P_E70)
    elif name.startswith("e80") or name == "mut-e80-sign":
        out["ret"] = w.run(P_E80)
    elif name.startswith("ef0"):
        out["ret"] = w.run(W_EF0, rcx=case.get("arg", 0))
    elif name.startswith("g-") or name == "mut-mode-neg":
        out["ret"] = w.run(G_4960, rcx=case.get("mode", 0))
    elif name.startswith("single"):
        out["ret"] = w.run(S_EBA40)
    elif name.startswith("sel") or name in ("mut-row18-2",
                                            "mut-nologo-long"):
        out["ret"] = w.run(S_BDF0, rcx=case.get("argc", 0),
                           rdx=w.argv_addr if "argv" in case else 0)
    gm = w.gm
    out["cells"] = {"flag": gm.d(FLAG), "supp": gm.d(SUPP),
                    "nologo": gm.d(NOLOGO), "clamp": gm.d(CLAMP),
                    "single": gm.q(SINGLE)}
    out.update(w.rets)
    out["ok"], out["fail"] = check(name, case, out)
    return out


def check(name, c, o):
    f = []
    tr = o["trace"]

    def eq(k, got, want):
        if got != want:
            f.append("%s: got %s want %s" % (k, hex(got), hex(want)))

    def tr_absent(t):
        if t in tr:
            f.append("unexpected trace: %s" % t)

    if name.startswith("da0") or name in ("mut-flag-neg",
                                          "mut-supp-neg"):
        # 0 iff flag set AND suppressor clear
        want = 0 if (c.get("flag") and not c.get("supp")) else 1
        eq("ret", o["ret"], want)
    elif name.startswith("ec0"):
        if not (c.get("flag") and not c.get("supp")):
            want = 1
        else:
            want = (~c.get("arg", 0)) & 1
        eq("ret", o["ret"], want)
    elif name.startswith("e70"):
        eq("ret", o["ret"], c.get("flag", 0) & 0xFFFFFFFF)
    elif name.startswith("e80") or name == "mut-e80-sign":
        if not (c.get("flag") and not c.get("supp")):
            want = 1
            tr_absent("a080"); tr_absent("a030")
        else:
            want = (c.get("c4ad8", 0) + c.get("c4aa8", 0)) & 0xFFFFFFFF
            if tr != ["a080", "a030"]:
                f.append("sub-call order: %s" % tr)
        eq("ret", o["ret"], want)
    elif name.startswith("ef0"):
        eq("supp", o["cells"]["supp"], c.get("arg", 0) & 0xFFFFFFFF)
    elif name.startswith("single"):
        if c.get("singleton", 1):
            eq("ret", o["ret"], HEAP + 0x4000)
            tr_absent("x10ec0"); tr_absent("xb190")
        else:
            eq("alloc_sz", o.get("alloc_sz", -1), 0x2E0)
            eq("b190_rcx", o.get("b190_rcx", -1), HEAP + 0xA000)
            eq("ret", o["ret"], HEAP + 0xA000)
            eq("single_wb", o["cells"]["single"], HEAP + 0xA000)
            if tr != ["eba40", "x10ec0", "xb190"]:
                f.append("lazy-init order: %s" % tr)
    elif name.startswith("g-") or name == "mut-mode-neg":
        # suppressor outcome
        flag, mode = c.get("flag", 0), c.get("mode", 0)
        stays = (flag == 0) or (mode == 1 and c.get("byte118", 0) == 0
                                and (c.get("gate9", 0) == 0
                                     or c.get("c4ad3", 0) == 1))
        eq("supp", o["cells"]["supp"], 1 if stays else 0)
        # ebx into the tail: mode on the flag==0 path, else 1
        want_ebx = mode if flag == 0 else 1
        eq("98e90_ecx", o.get("98e90_ecx", -1), want_ebx)
        eq("clamp", o["cells"]["clamp"],
           min(3, max(1, want_ebx)))
        if c.get("regobj"):
            eq("ea50_rdx", o.get("ea50_rdx", -1), RDXARG)
            eq("ea50_r8", o.get("ea50_r8", -1), want_ebx)
            eq("ea50_rcx", o.get("ea50_rcx", -1), HEAP + 0x7000)
        else:
            tr_absent("xea50")
        # ordering: ef0 first, e70 second; eba40 only when the
        # byte check is reached
        if tr[0:2] != ["ef0", "e70"]:
            f.append("head order: %s" % tr[:2])
        reach_byte = (flag != 0 and mode == 1
                      and (c.get("gate9", 0) == 0
                           or c.get("c4ad3", 0) == 1))
        if reach_byte:
            if "eba40" not in tr:
                f.append("byte check skipped unexpectedly")
        else:
            tr_absent("eba40")
    elif name.startswith("sel") or name in ("mut-row18-2",
                                            "mut-nologo-long"):
        eq("ddc0_ecx", o.get("ddc0_ecx", -1),
           1 if c.get("row18") == 1 else 0)
        want_nl = 1 if any(s == "-nologo" for s in c.get("argv", [])) \
            else 0
        eq("nologo", o["cells"]["nologo"], want_nl)
        if want_nl and "4de0" not in tr:
            f.append("nologo arg did not reach 314DE0")
        if not want_nl:
            tr_absent("4de0")
    return (len(f) == 0, f)


def main():
    raw, secs = load_image()
    C = {}

    # --- 001EDDA0: suppressor-first predicate ---
    C["da0-idle"] = {"flag": 0, "supp": 0}
    C["da0-supp"] = {"flag": 1, "supp": 1}
    C["da0-live"] = {"flag": 1, "supp": 0}
    C["da0-supp-only"] = {"flag": 0, "supp": 1}
    C["da0-flag2"] = {"flag": 2, "supp": 0}     # nonzero non-1 is "on"

    # --- 001EDEC0: flag-first predicate with argument ---
    C["ec0-idle"] = {"flag": 0, "supp": 0, "arg": 0}
    C["ec0-supp"] = {"flag": 1, "supp": 1, "arg": 1}
    C["ec0-arg0"] = {"flag": 1, "supp": 0, "arg": 0}
    C["ec0-arg1"] = {"flag": 1, "supp": 0, "arg": 1}
    C["ec0-arg2"] = {"flag": 1, "supp": 0, "arg": 2}
    C["ec0-arg3"] = {"flag": 1, "supp": 0, "arg": 3}

    # --- 001EDE70: verbatim flag ---
    C["e70-off"] = {"flag": 0}
    C["e70-on"] = {"flag": 1}
    C["e70-verbatim"] = {"flag": 0x7F}

    # --- 001EDE80: two-leaf sum ---
    C["e80-idle"] = {"flag": 0, "supp": 0}
    C["e80-supp"] = {"flag": 1, "supp": 1}
    C["e80-live"] = {"flag": 1, "supp": 0, "c4ad8": 5, "c4aa8": 7}
    C["e80-wrap"] = {"flag": 1, "supp": 0,
                     "c4ad8": 0xFFFFFFFF, "c4aa8": 2}

    # --- 001EDEF0: verbatim writer ---
    C["ef0-write7f"] = {"arg": 0x7F}
    C["ef0-write0"] = {"arg": 0}

    # --- 00184960: suppressor gate ---
    C["g-flag0-m1"] = {"flag": 0, "mode": 1}
    C["g-flag0-m0"] = {"flag": 0, "mode": 0}
    C["g-mode2"] = {"flag": 1, "mode": 2}
    C["g-m1-byte0"] = {"flag": 1, "mode": 1, "byte118": 0}
    C["g-m1-byte1"] = {"flag": 1, "mode": 1, "byte118": 1}
    C["g-m1-gatefail-byte0"] = {"flag": 1, "mode": 1, "gate9": 1,
                              "c4ad3": 2, "byte118": 0}
    C["g-m1-gatepass-byte0"] = {"flag": 1, "mode": 1, "gate9": 1,
                              "c4ad3": 1, "byte118": 0}
    C["g-m1-gatepass-byte1"] = {"flag": 1, "mode": 1, "gate9": 1,
                              "c4ad3": 1, "byte118": 1}
    C["g-m1-regobj"] = {"flag": 1, "mode": 1, "byte118": 1,
                        "regobj": 1}

    # --- 001EBA40: singleton getter ---
    C["single-present"] = {"singleton": 1}
    C["single-lazy"] = {"singleton": 0}

    # --- 0022BDF0: selector + -nologo scan ---
    C["sel-row0"] = {"row18": 0, "argc": 1, "argv": ["game"]}
    C["sel-row1"] = {"row18": 1, "argc": 1, "argv": ["game"]}
    C["sel-nologo"] = {"row18": 0, "argc": 1, "argv": ["-nologo"]}
    C["sel-nologo-suffix"] = {"row18": 0, "argc": 1,
                             "argv": ["-nologo2"]}
    C["sel-argc0"] = {"row18": 1, "argc": 0, "argv": []}
    C["sel-nologo-mid"] = {"row18": 0, "argc": 3,
                          "argv": ["x", "-nologo", "y"]}
    C["sel-nologo-partial"] = {"row18": 0, "argc": 1,
                              "argv": ["-nolo"]}

    # --- mutants ---
    C["mut-flag-neg"] = {"flag": 0xFFFFFFFF, "supp": 0}
    C["mut-supp-neg"] = {"flag": 1, "supp": 0x80000000}
    C["mut-row18-2"] = {"row18": 2, "argc": 1, "argv": ["g"]}
    C["mut-nologo-long"] = {"row18": 0, "argc": 1,
                            "argv": ["-nologoextra"]}
    C["mut-e80-sign"] = {"flag": 1, "supp": 0,
                         "c4ad8": 0x80000000, "c4aa8": 0}
    C["mut-mode-neg"] = {"flag": 1, "mode": 0xFFFFFFFF}

    results = {}
    fails = 0
    for name, case in C.items():
        results[name] = run_case(name, case, raw, secs)
        if not results[name]["ok"]:
            fails += 1
            print("FAIL %s: %s" % (name, results[name].get("fail")))
        else:
            print("ok   %s" % name)

    json.dump({"exe_sha256": SHA, "cases": results},
              open(RESULT, "w"), indent=1, default=str)
    print("== %d cases, %d failed ==" % (len(results), fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
