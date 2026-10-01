# EXP-092 — bazaar callee execution
#
# CONTRACT-bazaar-unlock-and-purchase.md section 13 ran 0030B180 (purchase),
# 0030B270 (refresh), 0030B570 (script-set) and 0030ADC0 (tally query) under
# diff_bazaar.py with THREE callees supplied as scripted oracles: the gate
# 00322C50, the tally write/read 003008A0, and the class record's own +0x50
# handler. Its UNKNOWN row: "what the three scripted callees do is NOT
# established". This harness re-drives all four entries with every callee
# running as shipped bytes.
#
#   REAL (shipped bytes, canonical VA):
#     0030B180  purchase: 00322C50(0x12,id) gate -> goods-row resolve
#               ([02EBF058]+0xC rva via 0020E600, stride word +8,
#               row = base32 + (id-0xD000)*stride) -> flags[id&0xFFF]+0x59C8
#               &= ~2 -> 003008A0(row+0x16/0x1A/0x1E, edx=0, r8=1, r9=3)
#     0030B270  refresh: row loop; per row the predicate — row+0x14 bit0 or
#               flag bit0 already set -> skip; flag bit1 -> skip; thresholds
#               +0x18/+0x1C/+0x20 all zero -> reject; loot queries +0x16/+0x1A
#               inlined (call [fam+0x50] with edx=3), +0x1E via 0030ADC0;
#               then flags+idx+0x59C8 |= 3
#     0030B570  script-set: id&0xF000==0xD000 -> 00322C50(1,id) -> row+0x14
#               bit1 gate -> flag = (old&~2)|((edx&1)<<1)
#     0030ADC0  tally query: 0xFFFF / nibble>0xE000 -> -1; idx>count-1 -> 0;
#               [fam+0x50]==0 -> 0; else jmp [fam+0x50] with edx=3
#     00322C50  kind dispatcher (ecx-1 indexes 0x323054; edx is the value):
#               kind 1 -> 00309440(id) -> fam+0x38 class number -> re-dispatch;
#               kind 0x12 -> bound 0xD000 <= id < 0xD000+[[02EBF058]+4]
#     00309440  class-number read: fam[id>>12]+0x38 dword (0x1EEBCF8 base)
#     003008A0  id op: 0xFFFF/0x1000/nibble>0xE000 -> -1; idx>fam+0x3C-1 ->
#               -1; ebp=famd(id,r9); esi=[fam+0x48](id,edx,r8,r9,arg5) or ebp;
#               r9==1 && ebp<=0 && esi>0 -> family range checks
#     00309F30  famd: same bounds (fail -> 0); edx==4 -> 002FD970; else
#               jmp [fam+0x50] or 0
#     002FD8D0  fam0/1/2 +0x50 reader: edx 0 -> (w&0x3FF)-(w>>0xA); 1 -> w>>0xA;
#               2 -> byte[fam+0x20+idx]; 3 -> w&0x3FF   (w = word[fam+8+idx*2])
#     002FD970  fam3/4/6/8/C +0x50 bitset reader (EXP-089 proven)
#     002FD150  fam0/1/2 +0x48 writer: r9 0/1/2 = u16 add/abs with clamps on
#               low10 vs hi6 fields; r9==3 = byte[fam+0x20+idx] write clamped
#               0..0x63 (r8!=0 -> absolute edx, r8==0 -> add)
#     002FD780  fam13 +0x48: gated r8==0 && r9==1 -> goods-row resolve and per-
#               loot 003008A0 calls (r9=1 absolute); else returns 0
#     002FD880  fam14 +0x48: gated r8==0 && r9==1 -> 00254EE0(00253690() +
#               (id&0xFFF)*edx) — the gil-bank write; else returns 0
#     0020E600  RVA->ptr: ecx + [01F83530]
#     00253690  read [[02092758]+8]; 00254EE0 clamp-write same field,
#               00316A50 notify only on nonzero delta (not exercised: cases
#               keep delta 0)
#
#   STUBBED (disclosed): none. IAT slots are zeroed (no IAT call on these
#   paths). Unreached: 002FD420 (fam3+ +0x48), 00325F40/0046A630 (its
#   callbacks), 00316A50 (00254EE0's delta!=0 path).
#
#   FIXTURE-PLANTED GLOBALS (disclosed):
#     [02EBF058]=REG   {+4 row count, +8 stride u16, +0xC row-table RVA}
#     [02EBF190]=FLAGS flag byte at +idx+0x59C8
#     [01F83530]=HEAP  0020E600 resolver base
#     [02092758]=GILB  {+8 bank dword} for 00253690/00254EE0
#     fam0/1/2 +8 -> u16 tally tables, +0x20 -> byte tables (runtime-null in
#     the shipped image; counts +0x3C and fnptrs +0x48/+0x50 are shipped data)
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

REG    = HEAP + 0x400000     # goods registry {+4 count, +8 stride, +0xC rva}
ROWS   = HEAP + 0x410000
FLAGS  = HEAP + 0x420000     # flag array; byte i at +i+0x59C8
GILB   = HEAP + 0x430000
F0U16  = HEAP + 0x440000
F0B    = HEAP + 0x450000
F1U16  = HEAP + 0x460000
F1B    = HEAP + 0x470000
F2U16  = HEAP + 0x480000
F2B    = HEAP + 0x490000

G_REG   = 0x2EBF058
G_FLAGS = 0x2EBF190
G_IMGB  = 0x1F83530          # 0020E600 base (bazaar paths, distinct from
                             # EXP-091's 0x1F85D30 reader)
G_GIL   = 0x2092758          # obj whose +8 is the bank field
FAMT    = 0x1EEBCC0
STRIDE  = 0x58
FLAGOFF = 0x59C8
ROWSTR  = 0x30

PURCHASE = 0x30B180
REFRESH  = 0x30B270
SETAVAIL = 0x30B570
TQUERY   = 0x30ADC0

CALLS = {
    0x30B180: "purchase", 0x30B270: "refresh",  0x30B570: "scriptset",
    0x30ADC0: "tquery",   0x322C50: "bound",    0x309440: "clsget",
    0x3008A0: "idop",     0x309F30: "famd",     0x2FD8D0: "r50a",
    0x2FD970: "bres",     0x2FD150: "w48a",     0x2FD880: "w48e",
    0x2FD780: "w48d",     0x2FD420: "w48c",     0x20E600: "imgadd",
    0x253690: "bankrd",   0x254EE0: "bankwr",   0x316A50: "upd",
    0x31EA90: "hx2",
}
BODYSTUBS = []               # no stubs: every reached body is shipped code

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)

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
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)

def goods_row(flags=0, l0=0x1001, t0=0, l1=0x1002, t1=0, l2=0x1003, t2=0):
    r = bytearray(ROWSTR)
    r[0x14] = flags & 0xFF
    struct.pack_into("<H", r, 0x16, l0 & 0xFFFF)
    struct.pack_into("<H", r, 0x1A, l1 & 0xFFFF)
    struct.pack_into("<H", r, 0x1E, l2 & 0xFFFF)
    r[0x18], r[0x1C], r[0x20] = t0 & 0xFF, t1 & 0xFF, t2 & 0xFF
    return bytes(r)

class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x600000), (STACK, 0x100000), (RETQ, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        if case.get("page0"):
            self.gm.map(0, 0x1000)

        gm.w(G_REG,   qw(case.get("reg", REG)))
        gm.w(G_FLAGS, qw(FLAGS))
        gm.w(G_IMGB,  qw(case.get("imgbase", HEAP)))
        gm.w(G_GIL,   qw(GILB))
        gm.w(GILB + 8, dw(case.get("bank", 0x1234)))

        # registry object: +4 row count, +8 stride, +0xC row-table RVA
        gm.w(REG + 4, dw(case.get("rows", 1)))
        gm.w(REG + 8, hw(case.get("stride", ROWSTR)))
        gm.w(REG + 0xC, dw(case.get("rowrva", ROWS - HEAP)))

        # goods rows
        for i, rw in enumerate(case.get("rowlist", [])):
            gm.w(ROWS + i * case.get("stride", ROWSTR), rw)

        # flag bytes: flagidx -> value at FLAGS + idx + 0x59C8
        for i, v in enumerate(case.get("flags", [])):
            gm.w(FLAGS + FLAGOFF + i, bytes([v & 0xFF]))

        # fam data pointers are runtime-null in the image; plant tables for
        # the fams the fixture's ids can reach (0/1/2 get u16+byte tables)
        for fam, (u16t, bt) in case.get("famtabs", {
                0: (F0U16, F0B), 1: (F1U16, F1B), 2: (F2U16, F2B)}).items():
            gm.w(FAMT + fam * STRIDE + 8,    qw(u16t))
            gm.w(FAMT + fam * STRIDE + 0x20, qw(bt))
        # u16 tally rows: (fam, idx) -> word value (low10 tally | hi6 cap)
        for (fam, idx), v in case.get("u16", {}).items():
            gm.w(case.get("famtabs", {}).get(fam,
                 {0: (F0U16, F0B), 1: (F1U16, F1B), 2: (F2U16, F2B)}[fam])[0]
                 + idx * 2, hw(v))
        for (fam, idx), v in case.get("bytetab", {}).items():
            gm.w(case.get("famtabs", {}).get(fam,
                 {0: (F0U16, F0B), 1: (F1U16, F1B), 2: (F2U16, F2B)}[fam])[1]
                 + idx, bytes([v & 0xFF]))

        for a, d in case.get("fill", []):
            gm.w(a, d)
        for va, data in case.get("patch", []):
            gm.w(va, data)

        self.trace, self.faults = [], []
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        name = CALLS[addr]
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8  = uc.reg_read(UC_X86_REG_R8)  & 0xFFFFFFFF
        r9  = uc.reg_read(UC_X86_REG_R9)  & 0xFFFFFFFF
        if addr == 0x3008A0:   # log full arg tuple incl. stack arg5
            sp = uc.reg_read(UC_X86_REG_RSP)
            a5 = struct.unpack("<Q", self.gm.r(sp + 0x28, 8))[0]
            self.trace.append((name, "id=%x" % (rcx & 0xFFFF),
                               "edx=%x" % rdx, "r8=%x" % r8, "r9=%x" % r9,
                               "a5=%x" % a5))
        elif addr == 0x322C50:
            self.trace.append((name, "kind=%x" % rcx, "val=%x" % rdx,
                               "r8=%x" % r8))
        elif addr == 0x309440:
            self.trace.append((name, "id=%x" % (rcx & 0xFFFF)))
        else:
            self.trace.append((name, "rcx=%x" % rcx, "rdx=%x" % rdx))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def build(case, raw, secs):
    return World(case, raw, secs)

def invoke(w, va, rcx=0, rdx=0, r8=0, r9=0, stack=()):
    uc, gm = w.uc, w.gm
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    for i, v in enumerate(stack):
        gm.w(sp + 0x28 + i * 8, qw(v))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, rcx)
    uc.reg_write(UC_X86_REG_RDX, rdx)
    uc.reg_write(UC_X86_REG_R8, r8)
    uc.reg_write(UC_X86_REG_R9, r9)
    try:
        uc.emu_start(va, RETQ, count=16_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    return uc.reg_read(UC_X86_REG_RAX)

def expect(name, snap, cond, why):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name + ("  -- " + why if not ok else ""))
    return ok

def flagbyte(i):  return FLAGS + FLAGOFF + i
def f1w(idx):     return F1U16 + idx * 2
def f1b(idx):     return F1B + idx

# ---- case list ---------------------------------------------------------------

def build_cases():
    C = []
    A = C.append
    def trhas(s, *names):
        return all(any(x[0] == n for x in s["trace"]) for n in names)

    # --- 0030B180 purchase ----------------------------------------------------
    # gate first: kind 0x12 bounds id to [0xD000, 0xD000 + rows)
    A({"name": "pur-gate-pass", "entry": PURCHASE, "rcx": 0xD000,
       "rowlist": [goods_row(l0=0x1001, l1=0x1002, l2=0x1003)],
       "flags": [3], "bytetab": {(1, 1): 7, (1, 2): 9, (1, 3): 4},
       "memprobe": [(flagbyte(0), 1), (f1b(1), 3)],
       "check": lambda s: s["rets"][0] == "0x1" and
                          s["mem"][0][1] == "01" and
                          s["mem"][1][1] == "000000" and
                          trhas(s, "bound", "imgadd", "idop")})
    A({"name": "pur-gate-fail", "entry": PURCHASE, "rcx": 0xD001,
       "rows": 1, "rowlist": [goods_row()], "flags": [3],
       "memprobe": [(flagbyte(0), 1), (f1b(1), 3)],
       "check": lambda s: s["rets"][0] == "0x0" and
                          s["mem"][0][1] == "03" and
                          not any(x[0] == "idop" for x in s["trace"])})
    A({"name": "pur-bound-hi", "entry": PURCHASE, "rcx": 0xD003,
       "rows": 4, "rowlist": [goods_row() for _ in range(4)], "flags": [0] * 4,
       "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "pur-bound-hi-fail", "entry": PURCHASE, "rcx": 0xD004,
       "rows": 4, "rowlist": [goods_row() for _ in range(4)], "flags": [0] * 4,
       "check": lambda s: s["rets"][0] == "0x0"})
    # purchase clears bit1 only, from every prior state
    for f in range(4):
        A({"name": "pur-flag%d" % f, "entry": PURCHASE, "rcx": 0xD000,
           "rowlist": [goods_row()], "flags": [f],
           "memprobe": [(flagbyte(0), 1)],
           "check": lambda s, f=f: s["rets"][0] == "0x1" and
                                   s["mem"][0][1] == "%02x" % (f & 1)})
    # null registry -> bound fails before row deref (returns 0, no fault)
    A({"name": "pur-nullreg", "entry": PURCHASE, "rcx": 0xD000,
       "reg": 0,
       "check": lambda s: s["rets"][0] == "0x0" and not s["faults"]})
    # row pointer resolves to 0 (empty RVA + zero resolver base) -> the
    # shipped body derefs word[0+0x16] unguarded: genuine fault input
    A({"name": "pur-nullrow", "entry": PURCHASE, "rcx": 0xD000,
       "rowrva": 0, "imgbase": 0, "expect_fault": True,
       "check": lambda s: any(f[0] == "MEM" and f[1] == "0x16"
                              for f in s["faults"])})
    # the three tally calls are absolute-zero writes on fam+0x20 bytes
    A({"name": "pur-tally-zero", "entry": PURCHASE, "rcx": 0xD000,
       "rowlist": [goods_row(l0=0x1005, l1=0x1007, l2=0x1009)],
       "bytetab": {(1, 5): 9, (1, 7): 8, (1, 9): 6, (1, 6): 3},
       "memprobe": [(f1b(5), 1), (f1b(6), 1), (f1b(7), 1), (f1b(9), 1)],
       "check": lambda s: s["rets"][0] == "0x1" and
                          s["mem"][0][1] == "00" and s["mem"][1][1] == "03" and
                          s["mem"][2][1] == "00" and s["mem"][3][1] == "00" and
                          [x[0] for x in s["trace"]].count("idop") == 3})
    # fam13 loot id: +0x48 = 0x2FD780 gated r8==0&&r9==1; purchase passes
    # r8=1,r9=3 -> real handler returns 0 without writing
    A({"name": "pur-famd-loot", "entry": PURCHASE, "rcx": 0xD000,
       "rowlist": [goods_row(l0=0xD005, l1=0xD006, l2=0xD007)],
       "bytetab": {},
       "memprobe": [(f1b(5), 1)],
       "check": lambda s: s["rets"][0] == "0x1" and
                          s["mem"][0][1] == "00" and
                          any(x[0] == "w48d" for x in s["trace"])})

    # --- 0030B270 refresh -----------------------------------------------------
    def refcase(name, **kw):
        c = {"name": name, "entry": REFRESH}
        c.update(kw)
        return c
    # refresh queries byte[fam+0x20 + idx] via +0x50 edx=3 — the same byte
    # table purchase zeroes
    B1 = {(1, 1): 5, (1, 2): 5, (1, 3): 5}
    A(refcase("ref-accept", rowlist=[goods_row(t0=1, t1=1, t2=1)],
              bytetab=B1, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "03"))
    A(refcase("ref-tally0", rowlist=[goods_row(t0=1, t1=1, t2=1)],
              bytetab={(1, 2): 5, (1, 3): 5}, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "00"))
    # clause 3: all thresholds zero -> rejected even with tallies present
    A(refcase("ref-allzero", rowlist=[goods_row(t0=0, t1=0, t2=0)],
              bytetab=B1, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "00"))
    # one threshold non-zero, its tally met, other loots query 0>=0 via fam13
    # (+0x50 null -> ecx=0)
    A(refcase("ref-one-t", rowlist=[goods_row(t0=1, l1=0xD001, l2=0xD002)],
              bytetab={(1, 1): 5}, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "03"))
    # clause 1: row+0x14 bit0 set (repeatable) skips the flag-bit0 test
    A(refcase("ref-repeat", rowlist=[goods_row(flags=1, t0=1, t1=1, t2=1)],
              bytetab=B1, flags=[1],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "03"))
    A(refcase("ref-repeat-fail", rowlist=[goods_row(flags=0, t0=1, t1=1, t2=1)],
              bytetab=B1, flags=[1],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "01"))
    # clause 2: already available (bit1) -> skip
    A(refcase("ref-avail", rowlist=[goods_row(t0=1, t1=1, t2=1)],
              bytetab=B1, flags=[2],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "02"))
    # sentinel loot id -> -1 < threshold -> fails
    A(refcase("ref-sentinel", rowlist=[goods_row(l0=0xFFFF, t0=1, t1=1, t2=1)],
              bytetab={(1, 2): 5, (1, 3): 5}, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "00"))
    # idx beyond fam1 count (0x1A4) -> 0 -> fails when threshold nonzero
    A(refcase("ref-oob", rowlist=[goods_row(l0=0x1200, t0=1, t1=1, t2=1)],
              bytetab={(1, 2): 5, (1, 3): 5}, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "00"))
    # threshold equal to tally is accepted (>= compare)
    A(refcase("ref-eq", rowlist=[goods_row(t0=5, t1=1, t2=1)],
              bytetab=B1, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "03"))
    # multi-row: row flags/flag bytes per index
    A(refcase("ref-multi", rows=4,
              rowlist=[goods_row(t0=1, t1=1, t2=1) for _ in range(4)],
              bytetab=B1,
              flags=[0, 2, 1, 0],
              memprobe=[(flagbyte(0), 1), (flagbyte(1), 1), (flagbyte(2), 1),
                        (flagbyte(3), 1)],
              check=lambda s: s["mem"][0][1] == "03" and
                              s["mem"][1][1] == "02" and
                              s["mem"][2][1] == "01" and
                              s["mem"][3][1] == "03"))
    # null registry -> count 0 -> loop skipped, nothing written
    A(refcase("ref-noreg", reg=0, rowlist=[goods_row(t0=1, t1=1, t2=1)],
              bytetab=B1, flags=[0],
              memprobe=[(flagbyte(0), 1)],
              check=lambda s: s["mem"][0][1] == "00" and
                              not s["faults"]))
    # trace: refresh calls the +0x50 handler directly (edx=3) and 0030ADC0
    # for the third loot
    A(refcase("ref-order", rowlist=[goods_row(t0=1, t1=1, t2=1)],
              bytetab=B1, flags=[0],
              check=lambda s: [x[0] for x in s["trace"]].count("r50a") == 3 and
                              any(x[0] == "tquery" for x in s["trace"])))

    # --- 0030B570 script-set ----------------------------------------------------
    A({"name": "set-avail", "entry": SETAVAIL, "rcx": 0xD000, "rdx": 1,
       "rowlist": [goods_row(flags=2)], "flags": [0],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "02" and
                          trhas(s, "bound", "clsget", "imgadd")})
    A({"name": "set-clear", "entry": SETAVAIL, "rcx": 0xD000, "rdx": 0,
       "rowlist": [goods_row(flags=2)], "flags": [3],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "01"})
    A({"name": "set-rowgate", "entry": SETAVAIL, "rcx": 0xD000, "rdx": 1,
       "rowlist": [goods_row(flags=1)], "flags": [0],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "00"})
    A({"name": "set-wrongfam", "entry": SETAVAIL, "rcx": 0xE000, "rdx": 1,
       "rowlist": [goods_row(flags=2)], "flags": [0],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "00" and
                          not any(x[0] == "bound" for x in s["trace"])})
    A({"name": "set-oob", "entry": SETAVAIL, "rcx": 0xD001, "rdx": 1,
       "rows": 1, "rowlist": [goods_row(flags=2)], "flags": [0, 0],
       "memprobe": [(flagbyte(1), 1)],
       "check": lambda s: s["mem"][0][1] == "00"})
    # null registry: gate fails first (empty window), no fault
    A({"name": "set-nullreg", "entry": SETAVAIL, "rcx": 0xD000, "rdx": 1,
       "reg": 0, "rowlist": [goods_row(flags=2)], "flags": [0],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "00" and not s["faults"]})
    # null row pointer (empty RVA + zero base): unguarded +0x14 deref
    A({"name": "set-nullrow", "entry": SETAVAIL, "rcx": 0xD000, "rdx": 1,
       "rowrva": 0, "imgbase": 0, "rowlist": [goods_row(flags=2)],
       "expect_fault": True,
       "check": lambda s: any(f[0] == "MEM" and f[1] == "0x14"
                              for f in s["faults"])})
    # bit0 of the flag byte is not consulted by script-set
    A({"name": "set-bit0free", "entry": SETAVAIL, "rcx": 0xD000, "rdx": 1,
       "rowlist": [goods_row(flags=2)], "flags": [1],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "03"})

    # --- 0030ADC0 tally query ----------------------------------------------------
    # edx=3 arm -> byte[fam+0x20 + idx]
    A({"name": "tq-read", "entry": TQUERY, "rcx": 0x1007,
       "bytetab": {(1, 7): 0x2A},
       "check": lambda s: s["rets"][0] == "0x2a" and
                          trhas(s, "r50a")})
    A({"name": "tq-byte-full", "entry": TQUERY, "rcx": 0x1007,
       "bytetab": {(1, 7): 0xFF},
       "check": lambda s: s["rets"][0] == "0xff"})
    A({"name": "tq-sentinel", "entry": TQUERY, "rcx": 0xFFFF,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "tq-highnib", "entry": TQUERY, "rcx": 0xF001,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "tq-e000", "entry": TQUERY, "rcx": 0xE000,
       "check": lambda s: s["rets"][0] == "0x0"})   # fam14 +0x50 null
    A({"name": "tq-nohandler", "entry": TQUERY, "rcx": 0xD001,
       "check": lambda s: s["rets"][0] == "0x0"})   # fam13 +0x50 null
    A({"name": "tq-oob", "entry": TQUERY, "rcx": 0x11A4,
       "check": lambda s: s["rets"][0] == "0x0"})   # fam1 idx == count 0x1A4
    A({"name": "tq-edge", "entry": TQUERY, "rcx": 0x11A3,
       "bytetab": {(1, 0x1A3): 0x11},
       "check": lambda s: s["rets"][0] == "0x11"})
    # edx is dead: caller's value collapses to 3 before the tail jump
    A({"name": "tq-deadarg", "entry": TQUERY, "rcx": 0x1007, "rdx": 0xDEAD,
       "bytetab": {(1, 7): 0x2A},
       "check": lambda s: s["rets"][0] == "0x2a" and
                          any(x[0] == "r50a" and x[2] == "rdx=3"
                              for x in s["trace"])})
    # fam with +0x50 null but byte table present: still 0 (handler gate first)
    A({"name": "tq-nohandler-tab", "entry": TQUERY, "rcx": 0xD001,
       "check": lambda s: s["rets"][0] == "0x0"})

    # --- 003008A0 standalone: the real write semantics ----------------------------
    # r9==1 u16 arm measured: new_low10 < hi6 -> writes hi6 (clamps UP to the
    # hi6 field); new >= hi6 -> writes min(new, 0x63). famd(r9=1) pre-read is
    # the low10; the r9==1&&ebp<=0&&esi>0 range-check clause never fires for
    # fam1 (ebp = low10 > 0 path differs).
    A({"name": "sg-add-under", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 5,
       "r8": 0, "r9": 1, "u16": {(1, 5): 3 | (0x14 << 10)},
       "memprobe": [(f1w(5), 2)],
       "check": lambda s: s["rets"][0] == "0x14" and
                          s["mem"][0][1] == hw(0x14 | (0x14 << 10)).hex()})
    A({"name": "sg-add-over", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 10,
       "r8": 0, "r9": 1, "u16": {(1, 5): 0x10 | (0x14 << 10)},
       "memprobe": [(f1w(5), 2)],
       "check": lambda s: s["rets"][0] == "0x1a" and
                          s["mem"][0][1] == hw(0x1A | (0x14 << 10)).hex()})
    A({"name": "sg-add-clamp99", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 100,
       "r8": 0, "r9": 1, "u16": {(1, 5): 0x10 | (0x14 << 10)},
       "memprobe": [(f1w(5), 2)],
       "check": lambda s: s["rets"][0] == "0x63" and
                          s["mem"][0][1] == hw(0x63 | (0x14 << 10)).hex()})
    A({"name": "sg-abs", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 0x30,
       "r8": 1, "r9": 1, "u16": {(1, 5): 3 | (0x14 << 10)},
       "memprobe": [(f1w(5), 2)],
       "check": lambda s: s["rets"][0] == "0x30" and
                          s["mem"][0][1] == hw(0x30 | (0x14 << 10)).hex()})
    # purchase's own call shape: r8=1 r9=3 -> byte-table absolute write
    A({"name": "sg-byte-zero", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 0,
       "r8": 1, "r9": 3, "bytetab": {(1, 5): 7},
       "memprobe": [(f1b(5), 1)],
       "check": lambda s: s["mem"][0][1] == "00"})
    A({"name": "sg-byte-add", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 5,
       "r8": 0, "r9": 3, "bytetab": {(1, 5): 7},
       "memprobe": [(f1b(5), 1)],
       "check": lambda s: s["mem"][0][1] == "0c"})
    A({"name": "sg-byte-clamp", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 5,
       "r8": 0, "r9": 3, "bytetab": {(1, 5): 0x60},
       "memprobe": [(f1b(5), 1)],
       "check": lambda s: s["mem"][0][1] == "63"})
    # fam13 +0x48 = 0x2FD780: gate-fail returns 0
    A({"name": "sg-famd-gate", "entry": 0x3008A0, "rcx": 0xD005, "rdx": 0,
       "r8": 1, "r9": 3,
       "check": lambda s: s["rets"][0] == "0x0" and
                          any(x[0] == "w48d" for x in s["trace"])})
    # fam14 +0x48 = 0x2FD880 (r8==0 && r9==1): bank write base+idx*edx;
    # idx 0 -> writes current bank back, no 00316A50
    A({"name": "sg-fame-bank", "entry": 0x3008A0, "rcx": 0xE000, "rdx": 5,
       "r8": 0, "r9": 1, "bank": 0x1234,
       "memprobe": [(GILB + 8, 4)],
       "check": lambda s: s["mem"][0][1] == dw(0x1234).hex() and
                          not any(x[0] == "upd" for x in s["trace"]) and
                          trhas(s, "w48e", "bankrd", "bankwr")})
    # sentinels / bounds
    A({"name": "sg-sentinel", "entry": 0x3008A0, "rcx": 0xFFFF, "rdx": 1,
       "r8": 0, "r9": 1,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "sg-oob", "entry": 0x3008A0, "rcx": 0x11A4, "rdx": 1,
       "r8": 0, "r9": 1,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    # r9=4 -> famd tail-jumps the bitset resolver unconditionally
    A({"name": "sg-r9-4", "entry": 0x3008A0, "rcx": 0x1005, "rdx": 0,
       "r8": 0, "r9": 4, "u16": {(1, 5): 3 | (0x14 << 10)},
       "check": lambda s: s["rets"][0] == "0x0" and
                          any(x[0] == "famd" for x in s["trace"])})

    # --- 00309F30 direct: the +0x50 edx arms -------------------------------------
    # edx 0 -> (w&0x3FF)-(w>>0xA); 1 -> w&0x3FF; 2 -> w>>0xA; 3 -> byte tab
    A({"name": "famd-d0", "entry": 0x309F30, "rcx": 0x1005, "rdx": 0,
       "u16": {(1, 5): 3 | (0x14 << 10)},
       "check": lambda s: s["rets"][0] == "0xffffffef"})   # 3 - 20
    A({"name": "famd-d1", "entry": 0x309F30, "rcx": 0x1005, "rdx": 1,
       "u16": {(1, 5): 3 | (0x14 << 10)},
       "check": lambda s: s["rets"][0] == "0x3"})
    A({"name": "famd-d2", "entry": 0x309F30, "rcx": 0x1005, "rdx": 2,
       "u16": {(1, 5): 3 | (0x14 << 10)},
       "check": lambda s: s["rets"][0] == "0x14"})
    A({"name": "famd-d3", "entry": 0x309F30, "rcx": 0x1005, "rdx": 3,
       "bytetab": {(1, 5): 0x2B},
       "check": lambda s: s["rets"][0] == "0x2b"})
    A({"name": "famd-d5", "entry": 0x309F30, "rcx": 0x1005, "rdx": 5,
       "u16": {(1, 5): 3 | (0x14 << 10)},
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "famd-oob", "entry": 0x309F30, "rcx": 0x11A4, "rdx": 1,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "famd-sentinel", "entry": 0x309F30, "rcx": 0xFFFF, "rdx": 1,
       "check": lambda s: s["rets"][0] == "0xffffffff"})
    A({"name": "famd-highnib", "entry": 0x309F30, "rcx": 0xF001, "rdx": 1,
       "check": lambda s: s["rets"][0] == "0xffffffff"})

    # --- 00322C50 dispatcher measured directly -----------------------------------
    A({"name": "bnd-k12-in", "entry": 0x322C50, "rcx": 0x12, "rdx": 0xD000,
       "rows": 3,
       "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "bnd-k12-edge", "entry": 0x322C50, "rcx": 0x12, "rdx": 0xD002,
       "rows": 3,
       "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "bnd-k12-hi", "entry": 0x322C50, "rcx": 0x12, "rdx": 0xD003,
       "rows": 3,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "bnd-k12-lo", "entry": 0x322C50, "rcx": 0x12, "rdx": 0xCFFF,
       "rows": 3,
       "check": lambda s: s["rets"][0] == "0x0"})
    A({"name": "bnd-k12-noreg", "entry": 0x322C50, "rcx": 0x12, "rdx": 0xD000,
       "reg": 0,
       "check": lambda s: s["rets"][0] == "0x0"})   # empty window
    # kind 1 = class-number indirection: fam13 +0x38 == 0x12 -> arm 0x12
    A({"name": "bnd-k1-d000", "entry": 0x322C50, "rcx": 1, "rdx": 0xD000,
       "rows": 3,
       "check": lambda s: s["rets"][0] == "0x1" and
                          trhas(s, "clsget")})
    # fam14 +0x38 lo dword = 0x13 -> kind-1 redispatch lands on the 0x13 arm:
    # bound [0xE000, 0xEFFF) -> 0xE000 passes
    A({"name": "bnd-k1-e000", "entry": 0x322C50, "rcx": 1, "rdx": 0xE000,
       "rows": 3,
       "check": lambda s: s["rets"][0] == "0x1"})
    A({"name": "bnd-k1-efff", "entry": 0x322C50, "rcx": 1, "rdx": 0xEFFF,
       "rows": 3,
       "check": lambda s: s["rets"][0] == "0x0"})   # EFFF is exclusive upper
    A({"name": "bnd-k0", "entry": 0x322C50, "rcx": 0, "rdx": 0xD000,
       "check": lambda s: s["rets"][0] == "0x0"})   # kind 0 -> eax=-1 -> reject
    A({"name": "bnd-k21", "entry": 0x322C50, "rcx": 0x21, "rdx": 0xD000,
       "check": lambda s: s["rets"][0] == "0x0"})   # kind > 0x20 -> reject

    # --- 00309440 class-number read ----------------------------------------------
    A({"name": "cls-d000", "entry": 0x309440, "rcx": 0xD000,
       "check": lambda s: s["rets"][0] == "0x12"})
    A({"name": "cls-1000", "entry": 0x309440, "rcx": 0x1000,
       "check": lambda s: s["rets"][0] == "0x6"})    # fam1 +0x38 lo = class 6
    A({"name": "cls-e000", "entry": 0x309440, "rcx": 0xE000,
       "check": lambda s: s["rets"][0] == "0x13"})   # fam14 +0x38 lo = 0x13
    A({"name": "cls-f000", "entry": 0x309440, "rcx": 0xF000,
       "check": lambda s: s["rets"][0] == "0xffffffff"})

    # --- purchase-then-refresh sequence (FZ-3 arithmetic) --------------------------
    # one-time row: refresh->3, purchase->1, refresh->clause1 blocks (bit0
    # set, row not repeatable) -> stays 1
    A({"name": "seq-one-time", "rowlist": [goods_row(t0=1, t1=1, t2=1)],
       "bytetab": {(1, 1): 5, (1, 2): 5, (1, 3): 5}, "flags": [0],
       "phases": [{"entry": REFRESH},
                  {"entry": PURCHASE, "rcx": 0xD000},
                  {"entry": REFRESH}],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "01"})
    # repeatable row: refresh->3, purchase->1 AND zeroes the three sold
    # bytes, so the third refresh runs the full predicate (r50a fires) but
    # fails the tally compare -> flag stays 1. The repeatable bit's effect is
    # visible in the trace (queries run), not the flag.
    A({"name": "seq-repeat", "rowlist": [goods_row(flags=1, t0=1, t1=1, t2=1)],
       "bytetab": {(1, 1): 5, (1, 2): 5, (1, 3): 5}, "flags": [0],
       "phases": [{"entry": REFRESH},
                  {"entry": PURCHASE, "rcx": 0xD000},
                  {"entry": REFRESH}],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "01" and
                          [x[0] for x in s["trace"]].count("r50a") == 7})
    # contrast: one-time row's third refresh skips at clause 1 — no queries
    A({"name": "seq-one-time-trace", "rowlist": [goods_row(t0=1, t1=1, t2=1)],
       "bytetab": {(1, 1): 5, (1, 2): 5, (1, 3): 5}, "flags": [0],
       "phases": [{"entry": REFRESH},
                  {"entry": PURCHASE, "rcx": 0xD000},
                  {"entry": REFRESH}],
       "memprobe": [(flagbyte(0), 1)],
       "check": lambda s: s["mem"][0][1] == "01" and
                          [x[0] for x in s["trace"]].count("r50a") == 6})

    # --- mutants ------------------------------------------------------------------
    M = []
    def mut(name, va, data, probe):
        M.append({"name": name, "patch": [(va, data)], "probe": probe})
    # arm-0x12 low bound 0xD000 -> 0xD001
    mut("mut-bound-d000->d001", 0x322F41, dw(0xD001), "pur-gate-pass")
    # purchase gate kind 0x12 -> 0x11 (different arm)
    mut("mut-purkind-12->11",   0x30B197, b"\x11", "pur-gate-pass")
    # 00309440 nibble bound 0xE -> 0xD (fam14 now out of range)
    mut("mut-clsget-e->d",      0x309448, b"\x0d", "cls-e000")
    # refresh or-byte 3 -> 1 (bit1 no longer raised)
    mut("mut-refresh-3->1",     0x30B467, b"\x01", "ref-accept")
    # purchase and-byte 0xFD -> 0xFF (bit1 never cleared)
    mut("mut-purclear-fd->ff",  0x30B209, b"\xff", "pur-flag3")
    # refresh threshold compare jl -> jge (result>=thresh now skips the row)
    mut("mut-thresh-jl->jge",   0x30B3DB, b"\x8d", "ref-accept")
    # script-set nibble 0xD000 -> 0xE000 (fam13 ids rejected)
    mut("mut-setnib-d->e",      0x30B58B, dw(0xE000), "set-avail")
    # script-set row gate test imm 2 -> 1
    mut("mut-setgate-2->1",     0x30B5FA, b"\x01", "set-avail")
    # +0x50 edx=1 u16 mask 0x3FF -> 0x3FE (odd low10 loses bit0)
    mut("mut-tally-3ff->3fe",   0x2FD93B, dw(0x3FE), "famd-d1")
    # +0x48 byte-arm written clamp constant 0x63 -> 0x62
    mut("mut-bclamp-63->62",    0x2FD20A, b"\x62", "sg-byte-clamp")
    # all-thresholds-zero reject: je -> jne
    mut("mut-allzero-je->jne",  0x30B370, b"\x85", "ref-allzero")

    return C, M

def main():
    raw, secs = load_image()
    cases, mutants = build_cases()
    by_name = {c["name"]: c for c in cases}
    results, npass = [], 0
    for c in cases:
        snap, w = run_case(c, raw, secs)
        snap["name"] = c["name"]
        results.append(snap)
        try:
            ok = c["check"](snap) and \
                 (c.get("expect_fault") or not snap["faults"])
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
        c["patch"] = list(c.get("patch", [])) + m["patch"]
        snap, w = run_case(c, raw, secs)
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

def run_case(case, raw, secs):
    w = build(case, raw, secs)
    rets = []
    for ph in case.get("phases", [{}]):
        rets.append(invoke(w, ph.get("entry", case.get("entry")),
                           rcx=ph.get("rcx", case.get("rcx", 0)),
                           rdx=ph.get("rdx", case.get("rdx", 0)),
                           r8=ph.get("r8", case.get("r8", 0)),
                           r9=ph.get("r9", case.get("r9", 0)),
                           stack=ph.get("stack", case.get("stack", ()))))
    gm = w.gm
    snap = {
        "rets": [hex(r & 0xFFFFFFFF) for r in rets],
        "rets64": [hex(r & 0xFFFFFFFFFFFFFFFF) for r in rets],
        "trace": [list(t) if isinstance(t, tuple) else t for t in w.trace],
        "faults": [list(f) if isinstance(f, tuple) else f for f in w.faults],
        "mem": [[hex(a), gm.r(a, n).hex()] for a, n in
                case.get("memprobe", [])],
    }
    return snap, w

if __name__ == "__main__":
    if len(sys.argv) > 1:
        raw, secs = load_image()
        cases, mutants = build_cases()
        for c in cases:
            if c["name"] == sys.argv[1]:
                snap, w = run_case(c, raw, secs)
                print(repr(snap))
                break
    else:
        sys.exit(0 if main() else 1)
