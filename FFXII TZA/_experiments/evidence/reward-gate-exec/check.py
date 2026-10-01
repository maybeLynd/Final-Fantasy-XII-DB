# EXP-090 — reward gate-callee execution
#
# CONTRACT-experience-and-licence-award.md section 13 ran 002F8BB0 (XP) and
# 002F90C0 (LP) under diff_reward_award.py with SIX callees supplied as
# scripted oracles: 0031B860 (find), 003135C0 (single-mode), 00313800
# (designated-member index), 00320AB0 (member-record resolve), 0031B810
# (party-slot unit), 00264150 (licence gate). Section 14's open question is
# exactly "what those six decide". This harness executes them — and their
# whole transitive call surface — as shipped bytes at canonical VAs.
#
#   REAL (shipped bytes, canonical VA) — the whole closure, ZERO stubs:
#     002F8BB0  XP gate+formula         002F90C0  LP gate+formula
#     0031B860  find unit by stats ptr  (callees 00236850 count leaf,
#               00236820 bounded getter: unit = [0x208E688]+i*0xF50,
#               match on unit+0x698 == arg)
#     003135C0  single-mode gate = (0030D9A0()==1)
#     0030D9A0  mode enum: dword [FRAME+0x5B04] bits -> 5/4/?/2/1/0
#     00377C20  bit-3 sub-question: u16[U16T+8+idx*2]>>15, idx=003148F0()
#     003148F0  index getter: clamp>=0 of [0x2EF2B0()+0x1044]
#     002EF2B0/002EF640  static chain -> 0x2164480
#     00313800  desig index: byte [FRAME+0x5AD5] -> 00320890 scan
#     00320890  u16-table scan FRAME+0x5A48+i*2, i<9 -> i / -1
#     00320AB0  resolve: 0031B9F0(idx,sel) byte -> rec FRAME+8+b*0x1C8 (b<=0x27)
#     0031B9F0  gate 00322C50(0x17,idx) then 5-arm byte read FRAME+idx*2+off
#               (off = 5A48/5A5A/5A6C/5A7E/5A90 by sel 0..4, else 0xFF)
#     0031B810  party slot: 00322C50(0x17,i) -> byte FRAME+i*2+0x5A5A -> 002367A0
#     002367A0  unit scan: 00322C50(2,id) gate then match word[stats+4]==id
#               (arg 0xFF -> compares 0xFFFF); count [0x208E6A0]
#     00322C50  32-arm bounds dispatcher; arms 2 (=[OBJD+4]) and 0x17 (=9)
#     00264150  licence gate: movsx byte [0x209A2A9]
#
#   STUBBED: nothing. Every reached body is shipped code over readable
#   globals; the only fixture content is guest memory.
#
#   FIXTURE-PLANTED GLOBALS (disclosed):
#     [0x2EBF190] = FRAME  the shared struct: stats records +8 (0x1C8 stride,
#                    0x28 slots), u16 tables +0x5A48/+0x5A5A/+0x5A6C/+0x5A7E/
#                    +0x5A90 (9 x u16, low byte used), mode flags +0x5B04,
#                    desig byte +0x5AD5
#     [0x208E688] = UNITS  unit array, stride 0xF50; +0x698 stats ptr,
#                    +0xE70/+0xE78 row ptrs
#     [0x208E6A0] = unit count (count leaf, getter bound, scan bound)
#     [0x2ADD100] = U16T   flag table {+4 count, +8 u16s, bit15}
#     [0x2EBF130] = OBJD   {+4 count} arm-2 bound for 00322C50
#     [0x21654C4] = index dword for 003148F0 (in-image, writable)
#     [0x209A2A9] = licence-gate byte (in-image, writable)
#     ROWS = {+0x34 dword xp fields, +0x2F byte lp fields}
#
# Memory: GuestMem host buffers via mem_map_ptr (EXP-087 finding: this host's
# unicorn DLLs intermittently fail uc_mem_write/read on mapped pages).

import ctypes, hashlib, json, struct, sys, os
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
BASE = 0x120000
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

FRAME  = HEAP + 0x020000      # [0x2EBF190] shared struct (>= 0x6000)
UNITS  = HEAP + 0x100000      # [0x208E688] unit array, stride 0xF50
U16T   = HEAP + 0x300000      # [0x2ADD100] flag table
OBJD   = HEAP + 0x310000      # [0x2EBF130] arm-2 bound object
ROW_E70 = HEAP + 0x320000     # corpse reward rows
ROW_E78 = HEAP + 0x321000

G_FRAME  = 0x2EBF190
G_UNITS  = 0x208E688
G_UCNT   = 0x208E6A0
G_U16T   = 0x2ADD100
G_OBJD   = 0x2EBF130
G_IDX    = 0x21654C4          # [0x2164280+0x200]+0x1044
G_LGATE  = 0x209A2A9

# frame struct offsets
F_RECS   = 0x8                # stats records, 0x1C8 stride
F_T0     = 0x5A48             # u16 tables: T0 desig-ids, T1 member-ids,
F_T1     = 0x5A5A             # T2 +0x5A6C, T3 +0x5A7E, T4 +0x5A90
F_T2     = 0x5A6C
F_T3     = 0x5A7E
F_T4     = 0x5A90
F_MODE   = 0x5B04             # mode flags dword
F_DESIG  = 0x5AD5             # designated byte

# unit / stats record field offsets
U_STATS  = 0x698
U_ROW70  = 0xE70
U_ROW78  = 0xE78
S_IDW    = 4                  # word read by 002367A0; bytes: id@+4, kind@+5
S_KIND   = 5
S_ID     = 4
S_M3C    = 0x3C
S_M64    = 0x64
S_B6B    = 0x6B
S_B7B    = 0x7B
S_L88    = 0x88
S_LVL    = 0x1C2
RECSZ    = 0x1C8
UNITSZ   = 0xF50

CALLS = {
    0x2F8BB0: "xp",       0x2F90C0: "lp",       0x31B860: "find",
    0x3135C0: "single",   0x30D9A0: "mode",     0x377C20: "flag77",
    0x3148F0: "idxget",   0x2EF2B0: "ef2b0",    0x2EF640: "ef640",
    0x313800: "desig",    0x320890: "dscan",    0x320AB0: "resolve",
    0x31B9F0: "b9f0",     0x31B810: "party",    0x2367A0: "uscan",
    0x322C50: "bound",    0x236850: "ucount",   0x236820: "uget",
    0x264150: "lgate",
}

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v

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
    iat_names = {}
    def rva2off(rva):
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + rs:
                return ra + rva - sva
        return None
    imp_dir = pe + 24 + (112 if struct.unpack_from("<H", raw, pe + 24)[0] == 0x20B else 96) + 8
    imp_rva, _ = struct.unpack_from("<2I", raw, imp_dir)
    off2 = rva2off(imp_rva)
    i = 0
    while True:
        ilt, ts, fwd, name_rva, iat_rva = struct.unpack_from("<5I", raw, off2 + 20 * i)
        if name_rva == 0:
            break
        dll = raw[rva2off(name_rva):].split(b"\0")[0].decode()
        ilt = ilt or iat_rva
        j = 0
        while True:
            e = struct.unpack_from("<Q", raw, rva2off(ilt) + 8 * j)[0]
            if e == 0:
                break
            if e >> 63:
                nm = "#%x" % (e & 0xffff)
            else:
                no = rva2off(e & 0x7FFFFFFF)
                nm = raw[no + 2:].split(b"\0")[0].decode()
            iat_names[BASE + iat_rva + 8 * j] = "%s!%s" % (dll, nm)
            j += 1
        i += 1
    return raw, secs, iat_names

class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), data, len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)

def stats_rec(idv=0, kind=0, m3c=0, m64=0, b6b=0, b7b=0, l88=0, lvl=0):
    r = bytearray(RECSZ)
    r[S_ID] = idv & 0xFF
    r[S_KIND] = kind & 0xFF
    struct.pack_into("<I", r, S_M3C, m3c & 0xFFFFFFFF)
    struct.pack_into("<I", r, S_M64, m64 & 0xFFFFFFFF)
    r[S_B6B] = b6b & 0xFF
    r[S_B7B] = b7b & 0xFF
    r[S_L88] = l88 & 0xFF
    r[S_LVL] = lvl & 0xFF
    return bytes(r)

class World:
    def __init__(self, case, raw, secs, iat_names):
        self.case = case
        self.iat_names = iat_names
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x800000), (STACK, 0x100000), (RETQ, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        # IAT slots -> zeros would fault on call; leave shipped values and trap
        # any call into unmapped import space via the unmapped hook.
        for slot in iat_names:
            gm.w(slot, qw(0))
        # globals
        gm.w(G_FRAME, qw(case.get("frame", FRAME)))
        gm.w(G_UNITS, qw(case.get("units", UNITS)))
        gm.w(G_UCNT,  dw(case.get("ucount", 0)))
        gm.w(G_U16T,  qw(case.get("u16t", U16T)))
        gm.w(G_OBJD,  qw(case.get("objd", OBJD)))
        gm.w(G_IDX,   dw(case.get("idx", 0)))
        gm.w(G_LGATE, bytes([case.get("lgate", 0) & 0xFF]))
        gm.w(OBJD + 4, dw(case.get("objd_count", 0)))
        # frame u16 tables: five 9-entry tables, low byte used
        for t, off in enumerate((F_T0, F_T1, F_T2, F_T3, F_T4)):
            for i, v in enumerate(case.get("t%d" % t, [])):
                gm.w(FRAME + off + i * 2, hw(v))
        gm.w(FRAME + F_MODE,  dw(case.get("mode", 0)))
        gm.w(FRAME + F_DESIG, bytes([case.get("desig", 0) & 0xFF]))
        # stats records at FRAME+8+k*0x1C8
        for i, rec in enumerate(case.get("recs", [])):
            gm.w(FRAME + F_RECS + i * RECSZ, rec)
        # flag table for 00377C20: 3-BYTE stride -- reads the u16 pair at
        # +8+i*3 and shifts bit15 down. count at +4.
        u16e = case.get("u16", [])
        gm.w(U16T + 4, dw(len(u16e)))
        for i, v in enumerate(u16e):
            gm.w(U16T + 8 + i * 3, hw(v))
        # units
        for i, u in enumerate(case.get("units_l", [])):
            gm.w(UNITS + i * UNITSZ, u)
        # corpse rows
        gm.w(ROW_E70 + 0x34, dw(case.get("e70_34", 0)))
        gm.w(ROW_E78 + 0x34, dw(case.get("e78_34", 0)))
        gm.w(ROW_E70 + 0x2F, bytes([case.get("e70_2f", 0) & 0xFF]))
        gm.w(ROW_E78 + 0x2F, bytes([case.get("e78_2f", 0) & 0xFF]))
        # per-case byte patches (mutants, disclosed)
        for va, data in case.get("patch", []):
            gm.w(va, data)
        self.trace, self.faults = [], []
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        self.trace.append((CALLS[addr], "rcx=%x" % uc.reg_read(UC_X86_REG_RCX),
                           "rdx=%x" % uc.reg_read(UC_X86_REG_RDX)))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def build(case, raw, secs, iat_names):
    return World(case, raw, secs, iat_names)

def invoke(w, va, rcx=0, rdx=0, r8=0, r9=0):
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    uc.reg_write(UC_X86_REG_R9, r9)
    try:
        uc.emu_start(va, RETQ, count=8_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    return uc.reg_read(UC_X86_REG_RAX)

def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

def unit(stats=0, row70=ROW_E70, row78=ROW_E78):
    u = bytearray(UNITSZ)
    struct.pack_into("<Q", u, U_STATS, stats)
    struct.pack_into("<Q", u, U_ROW70, row70)
    struct.pack_into("<Q", u, U_ROW78, row78)
    return bytes(u)

def rec_addr(k):  return FRAME + F_RECS + k * RECSZ
def unit_addr(i): return UNITS + i * UNITSZ

# ---- case list ---------------------------------------------------------------

def build_cases():
    C = []
    A = C.append

    # --- 00264150 licence gate: sign-extended byte -------------------------
    A({"name": "lgate-zero", "entry": 0x264150,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "lgate-pos", "entry": 0x264150, "lgate": 0x2A,
       "check": lambda s: s["rets"][0] == "0x2a"})
    A({"name": "lgate-neg", "entry": 0x264150, "lgate": 0xFF,
       "check": lambda s: s["rets"][0] == "0xffffffff"})

    # --- 00236850/00236820 unit count + bounded getter ----------------------
    A({"name": "uget-in", "entry": 0x236820, "rcx": 1, "ucount": 3,
       "check": lambda s: s["rets"][0] == hex(unit_addr(1))})
    A({"name": "uget-last", "entry": 0x236820, "rcx": 2, "ucount": 3,
       "check": lambda s: s["rets"][0] == hex(unit_addr(2))})
    A({"name": "uget-oob", "entry": 0x236820, "rcx": 3, "ucount": 3,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "uget-neg", "entry": 0x236820, "rcx": 0xFFFFFFFF, "ucount": 3,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "ucount", "entry": 0x236850, "ucount": 4,
       "check": lambda s: s["rets"][0] == "0x4"})

    # --- 0031B860 find unit by stats pointer --------------------------------
    sA, sB = rec_addr(2), rec_addr(5)
    A({"name": "find-hit", "entry": 0x31B860, "rcx": sB, "ucount": 3,
       "units_l": [unit(stats=sA), unit(stats=sA + 8), unit(stats=sB)],
       "check": lambda s: s["rets"][0] == hex(unit_addr(2))})
    A({"name": "find-miss", "entry": 0x31B860, "rcx": sB, "ucount": 2,
       "units_l": [unit(stats=sA), unit(stats=sA + 8)],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "find-null", "entry": 0x31B860, "rcx": 0, "ucount": 3,
       "units_l": [unit(stats=sA)],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "find-empty", "entry": 0x31B860, "rcx": sB, "ucount": 0,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "find-order", "entry": 0x31B860, "rcx": sB, "ucount": 3,
       "units_l": [unit(stats=sB), unit(stats=sB), unit(stats=sA)],
       "check": lambda s: s["rets"][0] == hex(unit_addr(0))})

    # --- 0030D9A0 mode enum + 003135C0 single gate --------------------------
    A({"name": "mode-0", "entry": 0x30D9A0, "mode": 0,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "mode-1", "entry": 0x30D9A0, "mode": 1,
       "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "mode-2", "entry": 0x30D9A0, "mode": 2,
       "check": lambda s: s["rets"][0] == "0x2"})
    A({"name": "mode-4", "entry": 0x30D9A0, "mode": 4,
       "check": lambda s: s["rets"][0] == "0x4"})
    A({"name": "mode-8", "entry": 0x30D9A0, "mode": 8,
       "check": lambda s: s["rets"][0] == "0x5"})
    A({"name": "mode-flagfn-set", "entry": 0x30D9A0, "mode": 0x10,
       "idx": 2, "u16": [0, 0, 0x8000],
       "check": lambda s: s["rets"][0] == "0x3"})
    A({"name": "mode-flagfn-clear", "entry": 0x30D9A0, "mode": 0x10,
       "idx": 2, "u16": [0, 0, 0x7FFF],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "mode-flagfn-oob", "entry": 0x30D9A0, "mode": 0x10,
       "idx": 9, "u16": [0x8000],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "mode-flags-3", "entry": 0x30D9A0, "mode": 3,
       "check": lambda s: s["rets"][0] == "0x2"})   # bit1 wins over bit0
    A({"name": "mode-flags-C", "entry": 0x30D9A0, "mode": 0xC,
       "check": lambda s: s["rets"][0] == "0x5"})   # bit3 wins over bit2
    A({"name": "mode-flags-18", "entry": 0x30D9A0, "mode": 0x18,
       "idx": 0, "u16": [0x8000],
       "check": lambda s: s["rets"][0] == "0x5"})   # bit3 wins over bit2+flagfn
    A({"name": "mode-flags-14", "entry": 0x30D9A0, "mode": 0x14,
       "idx": 0, "u16": [0x8000],
       "check": lambda s: s["rets"][0] == "0x4"})   # bit2 wins over flagfn
    A({"name": "single-yes", "entry": 0x3135C0, "mode": 1,
       "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "single-no-0", "entry": 0x3135C0, "mode": 0,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "single-no-5", "entry": 0x3135C0, "mode": 8,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "single-no-flagfn", "entry": 0x3135C0, "mode": 0x10,
       "idx": 0, "u16": [0x8000],
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 003148F0 index getter (clamp >=0) -----------------------------------
    A({"name": "idx-pos", "entry": 0x3148F0, "idx": 7,
       "check": lambda s: s["rets"][0] == "0x7"})
    A({"name": "idx-neg", "entry": 0x3148F0, "idx": 0xFFFFFFF9,
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 00313800 + 00320890 designated-index scan ---------------------------
    A({"name": "desig-hit0", "entry": 0x313800, "desig": 0x41,
       "t0": [0x41, 2, 3, 4, 5, 6, 7, 8, 9],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "desig-hit8", "entry": 0x313800, "desig": 9,
       "t0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
       "check": lambda s: s["rets"][0] == "0x8"})
    A({"name": "desig-miss", "entry": 0x313800, "desig": 0x7E,
       "t0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "desig-ff", "entry": 0x313800, "desig": 0xFF,
       "t0": [0xFF, 2, 3, 4, 5, 6, 7, 8, 9],
       "check": lambda s: s["rets"][0] == "0xffffffff"})  # 0xFF early-out wins
    A({"name": "desig-hibyte", "entry": 0x313800, "desig": 5,
       "t0": [1, 0x8105, 3, 4, 5, 6, 7, 8, 9],   # byte 5 at u16 index1 low byte
       "check": lambda s: s["rets"][0] == "0x1"})

    # --- 0031B9F0 byte getter: gate + 5-arm table select ---------------------
    for sel, off in enumerate((F_T0, F_T1, F_T2, F_T3, F_T4)):
        tag = "b9f0-sel%d" % sel
        case = {"name": tag, "entry": 0x31B9F0, "rcx": 3, "rdx": sel,
                "check": (lambda s, _v=0x40 + sel: s["rets"][0] == hex(_v))}
        for t in range(5):
            case["t%d" % t] = [0x40 + t] * 9
        A(case)
    A({"name": "b9f0-sel5", "entry": 0x31B9F0, "rcx": 3, "rdx": 5,
       "t0": [0x40] * 9, "check": lambda s: s["rets"][0] == "0xff"})
    A({"name": "b9f0-gate9", "entry": 0x31B9F0, "rcx": 9, "rdx": 0,
       "t0": [0x40] * 9, "check": lambda s: s["rets"][0] == "0xff"})
    A({"name": "b9f0-gate-neg", "entry": 0x31B9F0, "rcx": 0xFFFFFFFF, "rdx": 0,
       "t0": [0x40] * 9, "check": lambda s: s["rets"][0] == "0xff"})
    A({"name": "b9f0-idx8", "entry": 0x31B9F0, "rcx": 8, "rdx": 1,
       "t1": [1, 2, 3, 4, 5, 6, 7, 8, 0x55],
       "check": lambda s: s["rets"][0] == "0x55"})

    # --- 00322C50 bounds dispatcher (arms used here: 2 and 0x17) -------------
    A({"name": "bnd-k2-in", "entry": 0x322C50, "rcx": 2, "rdx": 4,
       "objd_count": 7, "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "bnd-k2-edge", "entry": 0x322C50, "rcx": 2, "rdx": 6,
       "objd_count": 7, "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "bnd-k2-oob", "entry": 0x322C50, "rcx": 2, "rdx": 7,
       "objd_count": 7, "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "bnd-k2-neg", "entry": 0x322C50, "rcx": 2, "rdx": 0xFFFFFFFF,
       "objd_count": 7, "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "bnd-k17-in", "entry": 0x322C50, "rcx": 0x17, "rdx": 8,
       "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "bnd-k17-oob", "entry": 0x322C50, "rcx": 0x17, "rdx": 9,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "bnd-k0", "entry": 0x322C50, "rcx": 0, "rdx": 0,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "bnd-k33", "entry": 0x322C50, "rcx": 0x21, "rdx": 0,
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 00320AB0 resolve: byte -> record ------------------------------------
    A({"name": "res-ok", "entry": 0x320AB0, "rcx": 2, "rdx": 1,
       "t1": [1, 2, 5, 4, 5, 6, 7, 8, 9],
       "check": lambda s: s["rets"][0] == hex(rec_addr(5))})
    A({"name": "res-b27", "entry": 0x320AB0, "rcx": 2, "rdx": 1,
       "t1": [1, 2, 0x27, 4, 5, 6, 7, 8, 9],
       "check": lambda s: s["rets"][0] == hex(rec_addr(0x27))})
    A({"name": "res-b28", "entry": 0x320AB0, "rcx": 2, "rdx": 1,
       "t1": [1, 2, 0x28, 4, 5, 6, 7, 8, 9],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "res-idx9", "entry": 0x320AB0, "rcx": 9, "rdx": 1,
       "t1": [1] * 9, "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "res-idxneg", "entry": 0x320AB0, "rcx": 0xFFFFFFFF, "rdx": 1,
       "t1": [1] * 9, "check": lambda s: s["rets"][0] == "0x0"})

    # --- 002367A0 unit scan by stats word id ----------------------------------
    A({"name": "uscan-hit", "entry": 0x2367A0, "rcx": 7, "objd_count": 0x20,
       "ucount": 3,
       "units_l": [unit(stats=rec_addr(0)), unit(stats=rec_addr(1)),
                   unit(stats=rec_addr(2))],
       "recs": [stats_rec(idv=3), stats_rec(idv=7), stats_rec(idv=9)],
       "check": lambda s: s["rets"][0] == hex(unit_addr(1))})
    A({"name": "uscan-miss", "entry": 0x2367A0, "rcx": 8, "objd_count": 0x20,
       "ucount": 3,
       "units_l": [unit(stats=rec_addr(0))],
       "recs": [stats_rec(idv=3)],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "uscan-ff", "entry": 0x2367A0, "rcx": 0xFF, "objd_count": 0x100,
       "ucount": 2,
       "units_l": [unit(stats=rec_addr(0)), unit(stats=rec_addr(1))],
       "recs": [stats_rec(idv=0xFF, kind=0), stats_rec(idv=0xFF, kind=0xFF)],
       # gate 2 passes 0xFF (bound 0x100); arg 0xFF then compares 0xFFFF,
       # matching only kind=0xFF,id=0xFF -- rec1, not rec0 (word 0x00FF)
       "check": lambda s: s["rets"][0] == hex(unit_addr(1))})
    A({"name": "uscan-gatefail", "entry": 0x2367A0, "rcx": 7, "objd_count": 3,
       "ucount": 3,
       "units_l": [unit(stats=rec_addr(0))],
       "recs": [stats_rec(idv=7)],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "uscan-nullstats", "entry": 0x2367A0, "rcx": 7, "objd_count": 0x20,
       "ucount": 2,
       "units_l": [unit(stats=0), unit(stats=rec_addr(1))],
       "recs": [stats_rec(idv=0), stats_rec(idv=7)],
       "check": lambda s: s["rets"][0] == hex(unit_addr(1))})

    # --- 0031B810 party slot -> member id -> unit -----------------------------
    A({"name": "party-hit", "entry": 0x31B810, "rcx": 1, "objd_count": 0x20,
       "t1": [3, 7, 5, 4, 5, 6, 7, 8, 9], "ucount": 3,
       "units_l": [unit(stats=rec_addr(0)), unit(stats=rec_addr(1)),
                   unit(stats=rec_addr(2))],
       "recs": [stats_rec(idv=3), stats_rec(idv=7), stats_rec(idv=5)],
       "check": lambda s: s["rets"][0] == hex(unit_addr(1))})
    A({"name": "party-gatefail", "entry": 0x31B810, "rcx": 9,
       "objd_count": 0x100, "ucount": 2,
       "units_l": [unit(stats=rec_addr(0)), unit(stats=rec_addr(1))],
       "recs": [stats_rec(idv=0xFF, kind=0xFF), stats_rec(idv=9)],
       # slot 9 fails the 9-slot gate -> 0xFF -> uscan arg -> 0xFFFF;
       # rec0 word = 0xFFFF -> matches
       "check": lambda s: s["rets"][0] == hex(unit_addr(0))})
    A({"name": "party-gatefail-nomatch", "entry": 0x31B810, "rcx": 9,
       "objd_count": 0x100, "ucount": 1,
       "units_l": [unit(stats=rec_addr(0))],
       "recs": [stats_rec(idv=9)],
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "party-memid-gatefail", "entry": 0x31B810, "rcx": 1,
       "objd_count": 3,
       "t1": [3, 7, 5, 4, 5, 6, 7, 8, 9], "ucount": 2,
       "units_l": [unit(stats=rec_addr(0))],
       "recs": [stats_rec(idv=7)],
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 002F8BB0 XP formula, all real callees --------------------------------
    # Recipient = record 5 (kind0, id3). A unit at index 1 carries it as
    # +0x698 so FIND passes. Corpse = unit 0, stats record 0x20 (kind1).
    def xp_fixture(**kw):
        recs = [stats_rec() for _ in range(0x28)]
        recs[5]    = kw.pop("rcp",  stats_rec(idv=3, kind=0))
        recs[0x20] = kw.pop("corpse", stats_rec(idv=9, kind=1, l88=1, lvl=0x10))
        case = {"entry": 0x2F8BB0, "rcx": rec_addr(5), "rdx": unit_addr(0),
                "mode": 1, "desig": 2,
                "t0": [0, 0, 2, 0, 0, 0, 0, 0, 0],
                "t1": [0, 0, 5, 0, 0, 0, 0, 0, 0],
                "ucount": 2, "objd_count": 0x20,
                "units_l": [unit(stats=rec_addr(0x20)),
                            unit(stats=rec_addr(5))],
                "recs": recs, "e70_34": 7, "e78_34": 5}
        case.update(kw)
        return case

    # award = (0x10 - 1) * 5 + 7 = 82 = 0x52
    A(dict(xp_fixture(), name="xp-single-hit",
           check=lambda s: s["rets"][0] == "0x52" and
           [t[0] for t in s["trace"]] ==
           ["xp", "find", "ucount", "uget", "ucount", "uget", "single",
            "mode", "flag77", "idxget", "ef2b0", "ef640", "desig", "dscan",
            "resolve", "b9f0", "bound"]))
    A(dict(xp_fixture(rcp=stats_rec(idv=3, kind=1)), name="xp-rcp-kind1",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(xp_fixture(rcp=stats_rec(idv=0x1B, kind=0)), name="xp-rcp-id1b",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(xp_fixture(rcp=stats_rec(idv=0x27, kind=0)), name="xp-rcp-id27",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(xp_fixture(rcp=stats_rec(idv=0x28, kind=0)), name="xp-rcp-id28",
           check=lambda s: s["rets"][0] == "0x52"))
    A(dict(xp_fixture(rcp=stats_rec(idv=3, kind=0, m64=1)), name="xp-rcp-mask0",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(xp_fixture(rcp=stats_rec(idv=3, kind=0, m3c=0x80000000)),
           name="xp-rcp-mask31", check=lambda s: s["rets"][0] == "0x0"))
    # FIND fails: no unit carries the recipient stats pointer
    A(dict(xp_fixture(), name="xp-rcp-nounit",
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(0x21))],
           check=lambda s: s["rets"][0] == "0x0"))
    # RESOLVE mismatches: T1[2] points at a different record than rdi
    A(dict(xp_fixture(), name="xp-desig-mismatch",
           t1=[0, 0, 6, 0, 0, 0, 0, 0, 0],
           check=lambda s: s["rets"][0] == "0x0"))
    # corpse gates
    A(dict(xp_fixture(), name="xp-corpse-null", rdx=0,
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(xp_fixture(), name="xp-corpse-nostats",
           units_l=[unit(stats=0), unit(stats=rec_addr(5))],
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(xp_fixture(corpse=stats_rec(idv=9, kind=0, l88=1, lvl=0x10)),
           name="xp-corpse-kind0",
           check=lambda s: s["rets"][0] == "0x0"))
    # recipient modifiers: bit3 doubles, bit5 zeroes (either bank)
    A(dict(xp_fixture(rcp=stats_rec(idv=3, kind=0, b6b=8)), name="xp-mod-dbl6b",
           check=lambda s: s["rets"][0] == "0xa4"))
    A(dict(xp_fixture(rcp=stats_rec(idv=3, kind=0, b7b=8)), name="xp-mod-dbl7b",
           check=lambda s: s["rets"][0] == "0xa4"))
    A(dict(xp_fixture(rcp=stats_rec(idv=3, kind=0, b6b=0x20)), name="xp-mod-zero",
           check=lambda s: s["rets"][0] == "0x0"))
    # negative pool: (0-2)*5 + 0 = -10 = 0xFFFFFFF6, carried by signed idiv path
    A(dict(xp_fixture(corpse=stats_rec(idv=9, kind=1, l88=2, lvl=0),
                      e70_34=0), name="xp-negative",
           check=lambda s: s["rets"][0] == "0xfffffff6"))

    # divided path: mode!=1 -> PARTY_FN(0..3) -> T1 member-id bytes -> units.
    # A member-id byte k can only match stats word[+4] = kind<<8|id when
    # kind==0 -- the real 002367A0 word compare makes kind-1 members
    # unreachable here (the scripted oracle admitted them; see record).
    def xp_div_fixture(**kw):
        recs = kw.pop("recs", [stats_rec() for _ in range(0x28)])
        if "rcp" in kw:
            recs[5] = kw.pop("rcp")
        if "corpse" in kw:
            recs[0x20] = kw.pop("corpse")
        case = {"entry": 0x2F8BB0, "rcx": rec_addr(5), "rdx": unit_addr(0),
                "mode": 2, "t1": [0xFF, 0xFF, 0xFF, 0xFF],
                "ucount": 2, "objd_count": 0x20,
                "units_l": [unit(stats=rec_addr(0x20)),
                            unit(stats=rec_addr(5))],
                "recs": recs, "e70_34": 7, "e78_34": 5}
        case.update(kw)
        return case

    # one eligible member (id 0x10, kind0) at slot 0 -> n=1 -> 82
    A(dict(xp_div_fixture(
           recs=[stats_rec() for _ in range(5)] +
                [stats_rec(idv=3, kind=0)] + [stats_rec()] * (0x20 - 6) +
                [stats_rec(idv=9, kind=1, l88=1, lvl=0x10)] +
                [stats_rec(idv=0x10, kind=0)] + [stats_rec()] * 6),
           t1=[0x10, 0xFF, 0xFF, 0xFF],
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(5)),
                    unit(stats=rec_addr(0x21))],
           ucount=3, name="xp-div-1",
           check=lambda s: s["rets"][0] == "0x52"))
    # two eligible members -> n=2 -> 41
    A(dict(xp_div_fixture(
           recs=[stats_rec() for _ in range(5)] +
                [stats_rec(idv=3, kind=0)] + [stats_rec()] * (0x20 - 6) +
                [stats_rec(idv=9, kind=1, l88=1, lvl=0x10)] +
                [stats_rec(idv=0x10, kind=0), stats_rec(idv=0x11, kind=0)] +
                [stats_rec()] * 5),
           t1=[0x10, 0x11, 0xFF, 0xFF],
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(5)),
                    unit(stats=rec_addr(0x21)), unit(stats=rec_addr(0x22))],
           ucount=4, name="xp-div-2",
           check=lambda s: s["rets"][0] == "0x29"))
    # no eligible members -> n=0 -> return 0 (before the divide)
    A(dict(xp_div_fixture(), name="xp-div-0",
           check=lambda s: s["rets"][0] == "0x0"))
    # member with id 0x1A kind0: eligible for XP as recipient filter but
    # SKIPPED by the divided-path member filter (kind0 && id==0x1A)
    A(dict(xp_div_fixture(
           recs=[stats_rec() for _ in range(5)] +
                [stats_rec(idv=3, kind=0)] + [stats_rec()] * (0x20 - 6) +
                [stats_rec(idv=9, kind=1, l88=1, lvl=0x10)] +
                [stats_rec(idv=0x1A, kind=0)] + [stats_rec()] * 6),
           t1=[0x1A, 0xFF, 0xFF, 0xFF],
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(5)),
                    unit(stats=rec_addr(0x21))],
           ucount=3, name="xp-div-skip-1a",
           check=lambda s: s["rets"][0] == "0x0"))
    # member id 0x19 kind0: counted (filter excludes only 0x1A + 0x1B..0x27)
    A(dict(xp_div_fixture(
           recs=[stats_rec() for _ in range(5)] +
                [stats_rec(idv=3, kind=0)] + [stats_rec()] * (0x20 - 6) +
                [stats_rec(idv=9, kind=1, l88=1, lvl=0x10)] +
                [stats_rec(idv=0x19, kind=0)] + [stats_rec()] * 6),
           t1=[0x19, 0xFF, 0xFF, 0xFF],
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(5)),
                    unit(stats=rec_addr(0x21))],
           ucount=3, name="xp-div-count-19",
           check=lambda s: s["rets"][0] == "0x52"))
    # masked member skipped
    A(dict(xp_div_fixture(
           recs=[stats_rec() for _ in range(5)] +
                [stats_rec(idv=3, kind=0)] + [stats_rec()] * (0x20 - 6) +
                [stats_rec(idv=9, kind=1, l88=1, lvl=0x10)] +
                [stats_rec(idv=0x10, kind=0, m64=1)] + [stats_rec()] * 6),
           t1=[0x10, 0xFF, 0xFF, 0xFF],
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(5)),
                    unit(stats=rec_addr(0x21))],
           ucount=3, name="xp-div-masked",
           check=lambda s: s["rets"][0] == "0x0"))
    # negative pool through the signed divide: -10 / 2 = -5
    A(dict(xp_div_fixture(
           corpse=stats_rec(idv=9, kind=1, l88=2, lvl=0), e70_34=0,
           recs=[stats_rec() for _ in range(5)] +
                [stats_rec(idv=3, kind=0)] + [stats_rec()] * (0x20 - 6) +
                [stats_rec(idv=9, kind=1, l88=2, lvl=0)] +
                [stats_rec(idv=0x10, kind=0), stats_rec(idv=0x11, kind=0)] +
                [stats_rec()] * 5),
           t1=[0x10, 0x11, 0xFF, 0xFF],
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(5)),
                    unit(stats=rec_addr(0x21)), unit(stats=rec_addr(0x22))],
           ucount=4, name="xp-div-neg",
           check=lambda s: s["rets"][0] == "0xfffffffb"))

    # --- 002F90C0 LP formula --------------------------------------------------
    def lp_fixture(**kw):
        recs = [stats_rec() for _ in range(0x28)]
        recs[5]    = kw.pop("rcp",  stats_rec(idv=3, kind=0))
        recs[0x20] = kw.pop("corpse", stats_rec(idv=9, kind=1, l88=1, lvl=0x10))
        case = {"entry": 0x2F90C0, "rcx": rec_addr(5), "rdx": unit_addr(0),
                "ucount": 2,
                "units_l": [unit(stats=rec_addr(0x20)),
                            unit(stats=rec_addr(5))],
                "recs": recs, "e70_2f": 7, "e78_2f": 5}
        case.update(kw)
        return case
    # award = (0x10-1)*5 + 7 = 82 = 0x52
    A(dict(lp_fixture(), name="lp-ok",
           check=lambda s: s["rets"][0] == "0x52" and
           [t[0] for t in s["trace"]][:2] == ["lp", "lgate"]))
    A(dict(lp_fixture(lgate=1), name="lp-gate-on",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(lp_fixture(rcp=stats_rec(idv=0x06, kind=0)), name="lp-id-06",
           check=lambda s: s["rets"][0] == "0x52"))
    A(dict(lp_fixture(rcp=stats_rec(idv=0x07, kind=0)), name="lp-id-07",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(lp_fixture(rcp=stats_rec(idv=0x1A, kind=0)), name="lp-id-1a",
           check=lambda s: s["rets"][0] == "0x52"))
    A(dict(lp_fixture(rcp=stats_rec(idv=0x27, kind=0)), name="lp-id-27",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(lp_fixture(rcp=stats_rec(idv=0x28, kind=0)), name="lp-id-28",
           check=lambda s: s["rets"][0] == "0x52"))
    A(dict(lp_fixture(rcp=stats_rec(idv=3, kind=0, b6b=0x10)), name="lp-mod-dbl",
           check=lambda s: s["rets"][0] == "0xa4"))
    # asymmetry: LP has no zeroing modifier - bit5 leaves the award standing
    A(dict(lp_fixture(rcp=stats_rec(idv=3, kind=0, b6b=0x20)), name="lp-mod-20",
           check=lambda s: s["rets"][0] == "0x52"))
    A(dict(lp_fixture(rcp=stats_rec(idv=3, kind=0, m64=2)), name="lp-mask1",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(lp_fixture(rcp=stats_rec(idv=3, kind=1)), name="lp-kind1",
           check=lambda s: s["rets"][0] == "0x0"))
    A(dict(lp_fixture(rcx=0), name="lp-rcp-null",
           check=lambda s: s["rets"][0] == "0x52"))
    A(dict(lp_fixture(rdx=0), name="lp-corpse-null",
           check=lambda s: s["rets"][0] == "0x0"))

    # --- mutants: byte patches on shipped bodies, detected by a case --------
    M = []
    def mut(name, va, data, probe):
        M.append({"name": name, "patch": [(va, data)], "probe": probe})
    mut("mut-find-698->699", 0x31B895, hw(0x699), "find-hit")
    mut("mut-single-1->2", 0x3135CD, b"\x02", "single-yes")
    mut("mut-mode-b3->b4", 0x30D9B3, b"\x10", "mode-8")
    mut("mut-dscan-9->8", 0x3208B5, b"\x08", "desig-hit8")
    mut("mut-b9f0-5a5a->5a5b", 0x31BA8F, dw(0x5A5B), "b9f0-sel1")
    mut("mut-arm17-9->8", 0x322FB0, dw(8), "bnd-k17-in")
    mut("mut-uscan-w4->w5", 0x2367E2, b"\x05", "uscan-hit")
    mut("mut-xpmask-3->2", 0x2F8C07, dw(0x80000002), "xp-rcp-mask0")
    mut("mut-div-4->3", 0x2F8CE4, b"\x03", "xp-div-3slot")
    mut("mut-lp-1a->1b", 0x2F90EC, b"\x1b", "lp-id-1a")

    # probe cases the mutants are measured against
    # the only eligible member sits at slot 3: mutating the loop bound
    # 4->3 skips it entirely.
    A(dict(xp_div_fixture(
           recs=[stats_rec() for _ in range(5)] +
                [stats_rec(idv=3, kind=0)] + [stats_rec()] * (0x20 - 6) +
                [stats_rec(idv=9, kind=1, l88=1, lvl=0x10)] +
                [stats_rec(idv=0x10, kind=0)] + [stats_rec()] * 6),
           t1=[0xFF, 0xFF, 0xFF, 0x10],
           units_l=[unit(stats=rec_addr(0x20)), unit(stats=rec_addr(5)),
                    unit(stats=rec_addr(0x21))],
           ucount=3, name="xp-div-3slot",
           check=lambda s: s["rets"][0] == "0x52"))
    return C, M

def main():
    raw, secs, iat_names = load_image()
    cases, mutants = build_cases()
    by_name = {c["name"]: c for c in cases}
    results, npass = [], 0
    for c in cases:
        snap, w = run_case(c, raw, secs, iat_names)
        snap["name"] = c["name"]
        results.append(snap)
        try:
            ok = c["check"](snap) and not snap["faults"]
        except Exception as e:
            ok = False
            snap["check_error"] = str(e)
        npass += ok
        expect(c["name"], snap, ok, repr(snap)[:400])
    print("%d/%d cases" % (npass, len(cases)))
    ndet = 0
    for m in mutants:
        probe = by_name[m["probe"]]
        c = dict(probe)
        c["patch"] = m["patch"]
        snap, w = run_case(c, raw, secs, iat_names)
        try:
            detected = not probe["check"](snap)
        except Exception:
            detected = True
        ndet += detected
        snap["name"] = m["name"]
        snap["detected"] = detected
        snap["probe"] = m["probe"]
        results.append(snap)
        expect(m["name"], snap, detected, repr(snap)[:300])
    print("%d/%d mutants detected" % (ndet, len(mutants)))
    out = {"exe_sha256": SHA, "image_base": hex(BASE),
           "cases": npass, "cases_total": len(cases),
           "mutants_detected": ndet, "mutants_total": len(mutants),
           "results": results}
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json"), "w").write(json.dumps(out, indent=1))
    return npass == len(cases) and ndet == len(mutants)

def run_case(case, raw, secs, iat_names):
    w = build(case, raw, secs, iat_names)
    rets = []
    for ph in case.get("phases", [{}]):
        rets.append(invoke(w, ph.get("entry", case.get("entry")),
                           rcx=ph.get("rcx", case.get("rcx", 0)),
                           rdx=ph.get("rdx", case.get("rdx", 0))))
    snap = {
        "rets": [hex(r & 0xFFFFFFFF) for r in rets],
        "rets64": [hex(r & 0xFFFFFFFFFFFFFFFF) for r in rets],
        "trace": [list(t) if isinstance(t, tuple) else t for t in w.trace],
        "faults": [list(f) if isinstance(f, tuple) else f for f in w.faults],
    }
    return snap, w

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # debug: run a single named case
        raw, secs, iat_names = load_image()
        cases, mutants = build_cases()
        for c in cases:
            if c["name"] == sys.argv[1]:
                snap, w = run_case(c, raw, secs, iat_names)
                print(repr(snap))
                break
    else:
        sys.exit(0 if main() else 1)
