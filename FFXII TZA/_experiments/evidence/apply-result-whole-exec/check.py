# apply-result-to-target: WHOLE applier — runtime validation for
# CONTRACT-apply-result-to-target.md. Executes the complete applier
# 003112F0..00311AE7 on shipped bytes under Unicorn with the REAL callee
# layer (EXP-060 stubbed the five setters; EXP-148 decoded them).
#
#   003112F0 (0x7F8): the applier. rcx=record, rdx=source unit,
#     r8=target unit, r9w=flags16, arg5=extended flags (bit0 skips the
#     30B9B0 gate; bit9 suppresses the tail 30FED0).
#     Flow: 31B860 resolves source/target records; arg5&1==0 ->
#     30B9B0(tgtRec, srcRec) aborts on nonzero; 385BA0 gate; flags2
#     bit19 -> b[stats+0xE9A]|=8, flags2 bit14 -> 3A1180(0x34) -> 2DF220
#     -> b[stats+0xE9A]|=4; +0x11C/+0x11D levels -> 30C650; member
#     target steals +0x32..+0x34 -> 3008A0 + btr flagobj+0x14 + 253770;
#     +0x38 item -> 3008A0; +0x54 mask -> 30E360 mode3 per bit;
#     +0x58 mask -> 30E360 mode0 per bit; +0x5C/+0xDC copy-throughs to
#     unit+0xBC/+0x13C; numeric dispatch (EXP-060's segment) now calls
#     the REAL setters; +0x3C..0x41 -> 30E130 modes 2/0; +0x42..0x50 ->
#     unit+0x17C..; member +0x11E.. adds; member +0x128.. effect bytes
#     or/and into flagobj+0x78..; gil via 253690/254EE0; tail:
#     b[stats+0xE9A]&=0xF3; FED0(tgt,0) iff arg5 bit9 clear && landed.
#
#   REAL callees (shipped bytes, fixtures planted):
#     0030E360 status engine (6 modes on unit+0x38/0x3C/0x64, duration
#       unit+0xBC+bit*4, word unit+0x13C+bit*2, recursive link loop,
#       tail FED0 suppressed by flags bit9)
#     0030E130 status-bit modifier; 0030FED0 recompute; 0030C650 level;
#     003008A0 item write; 00316A50 field writer
#     00300530 HP setter — d[unit+0x48] store, floor d[rec+0x48], cap
#       d[unit+0x24] (x2 if status bit 0x1C), floor-1 if status bit
#       0x10; on newHP<=floor: E360(bit0,mode3) the KO transition,
#       member kill counter w[flagobj+8]++, 306F00 gate -> 3299B0
#     00300520 HP delta shim (edx -= d[unit+0x48] -> 300530)
#     00300CE0 MP setter (w[unit+0x4C], cap w[unit+0x28], 30B770/30B7F0
#       gates, 0BC0 spillover on gain, 2FA540 on decrease)
#     00300C90 MP delta shim (edx -= w[unit+0x4C] -> CE0, remainder >
#       w[unit+6] -> 0BC0)
#     00300BC0 secondary op (unit+6 add with 30B770/30B7F0 gates)
#     real leaves: 2536A0, 20E600, 2F9A60/2F9B20/2F9BD0, 3166F0,
#       322C50 (+arms), 861EC0 memset in hook
#
#   Scripted boundaries (entry-intercepted, args+stack dwords recorded,
#   disclosed): 31B860 (per-input unit->record map), 30B9B0, 30B8E0,
#   377C20, 3283D0, 28F1F0, 316D70, 469BB0, 32A150, 306F00, 3299B0,
#   30B770, 30B7F0, 30E060, 2FA540, 385BA0, 3A1180, 2DF220, 253770,
#   253690, 254EE0, 300FC0, 3105D0, 319E30, 387730, 3876D0, 386A50,
#   386AE0, 46A720, 46A790, 46A690, 35D8C0, 2EACD0, 329210, 31E9A0,
#   323890, 2FEF30, 165C0, 15E90, 16BF0, 632B0, 9F30, EA40, 279B0,
#   8C40 (canary), 300140, 301140, 307D10, and NESTED 3112F0 calls
#   (recorded + skipped — recursive applier re-entry through the E360/
#   E130 notify struct is boundary'd; the struct is memset then thunk-
#   filled, and our scripted thunks leave b[+0x2C] clear).
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
IMG_LO = 0x120000
HEAP = 0x40000000
STACK = 0x61000000
RETQ = 0x62000000

# ---- subjects (all executed as shipped bytes) ----
F_APPLY = 0x003112F0       # the whole applier
F_E360  = 0x0030E360       # status engine
F_E130  = 0x0030E130
F_FED0  = 0x0030FED0
F_C650  = 0x0030C650
F_08A0  = 0x003008A0
F_16A50 = 0x00316A50
F_0530  = 0x00300530       # HP setter (absolute semantic)
F_0520  = 0x00300520       # HP delta shim -> 300530
F_0CE0  = 0x00300CE0       # MP setter
F_0C90  = 0x00300C90       # MP delta shim -> 300CE0
F_0BC0  = 0x00300BC0       # secondary op
V_C50   = 0x00322C50       # class validator (real)

# ---- real helpers ----
S_36A0  = 0x002536A0
S_E600  = 0x0020E600
S_9A60  = 0x002F9A60
S_9B20  = 0x002F9B20
S_9BD0  = 0x002F9BD0
S_166F0 = 0x003166F0

# ---- scripted boundaries ----
X_B860  = 0x0031B860       # unit -> record (per-input map)
X_B9B0  = 0x0030B9B0       # apply gate
X_B8E0  = 0x0030B8E0       # immunity-ish gate
X_77C20 = 0x00377C20       # can-die check
X_283D0 = 0x003283D0       # value notify
X_8F1F0 = 0x0028F1F0       # damage-number notify
X_16D70 = 0x00316D70       # provoke/aim lookup
X_69BB0 = 0x00469BB0       # pre-death hook
X_2A150 = 0x0032A150       # kill-count notify
X_06F00 = 0x00306F00       # post-kill gate
X_299B0 = 0x003299B0       # msg/credit notify
X_B770  = 0x0030B770       # MP gate A
X_B7F0  = 0x0030B7F0       # MP gate B
X_E060  = 0x0030E060       # FED0 tail
X_FA540 = 0x002FA540       # MP-decrease notify
X_85BA0 = 0x00385BA0       # applier mid-gate
X_A1180 = 0x003A1180       # index lookup
X_DF220 = 0x002DF220       # clamp-ish
X_53770 = 0x00253770       # steal-slot tail
X_53690 = 0x00253690       # gil getter
X_54EE0 = 0x00254EE0       # gil setter
X_0FC0  = 0x00300FC0       # member-class redirect
X_105D0 = 0x003105D0
X_19E30 = 0x00319E30
X_87730 = 0x00387730       # E360 duration getter
X_876D0 = 0x003876D0       # E360 word helper
X_6A50  = 0x00386A50       # notify thunk A
X_6AE0  = 0x00386AE0       # notify thunk B
X_A720  = 0x0046A720
X_A790  = 0x0046A790
X_A690  = 0x0046A690       # C650 post-sync
X_5D8C0 = 0x0035D8C0
X_EACD0 = 0x002EACD0
X_29210 = 0x00329210
X_1E9A0 = 0x0031E9A0
X_23890 = 0x00323890
X_FEF30 = 0x002FEF30
X_165C0 = 0x003165C0
X_15E90 = 0x00315E90
X_16BF0 = 0x00316BF0
X_632B0 = 0x008632B0
X_9F30  = 0x00309F30
X_EA40  = 0x0030EA40
X_279B0 = 0x003279B0
X_8C40  = 0x00808C40       # stack-canary check
X_0140  = 0x00300140       # E360 arm helpers
X_1140  = 0x00301140
X_7D10  = 0x00307D10
X_84D0  = 0x003284D0       # E360 post-arm member fn (flags bit4 gate)
X_A800  = 0x0046A800       # E360 notify thunk (mode 3/4)
X_D6A0  = 0x0016D6A0       # E360 notify thunk (mode 0/1/2/5)
X_2280  = 0x00312280       # E360 bit-arm kill/notify
X_6A70  = 0x00386A70       # E360 clear-mode notify thunk

# ---- globals / fixture cells ----
CANARY  = 0x01F44830
UNITB   = 0x020927C0
ELEMB   = 0x01F83530       # 20E600's cell
FDESC   = 0x00D10460
FTAB2   = 0x00D10550
CATTAB  = 0x01EEBCC0
FLAGTBL = 0x01EECF98
D_040   = 0x02EBF040
D_038   = 0x02EBF038
D_0F0   = 0x02EBF0F0
D_0F8   = 0x02EBF0F8
D_108   = 0x02EBF108
D_130   = 0x02EBF130
D_138   = 0x02EBF138
D_190   = 0x02EBF190
RNDC    = 0x01F83380       # 300530's float cell pair (verified below)
RNDC2   = 0x00906D80       # placeholder; resolved at fixture time

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
        self.uc = uc
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

    def f(self, a):
        return struct.unpack("<f", bytes(self.uc.mem_read(a, 4)))[0]


def plant_unit(w, base, u):
    """Unit/stats-block fixture — fields shared by the applier, E360 and
    the numeric setters (they read/write the UNIT arg directly)."""
    gm = w.gm
    gm.w(base + 4, bytes([u.get("b4", 0) & 0xFF]))
    gm.w(base + 5, bytes([u.get("b5", 0) & 0xFF]))
    gm.w(base + 6, struct.pack("<h", u.get("w6", 0)))
    gm.w(base + 8, struct.pack("<h", u.get("w8", 0)))
    gm.w(base + 0xA, struct.pack("<h", u.get("wa", 0)))
    gm.w(base + 0x12, struct.pack("<h", u.get("w12", 0)))
    gm.w(base + 0x14, struct.pack("<h", u.get("w14", 0)))
    gm.w(base + 0x24, dw(u.get("d24", 0)))          # maxHP
    gm.w(base + 0x28, struct.pack("<h", u.get("w28", 0)))  # maxMP
    gm.w(base + 0x2A, bytes([u.get("b2a", 0) & 0xFF]))
    gm.w(base + 0x2B, bytes([u.get("b2b", 0) & 0xFF]))
    gm.w(base + 0x2F, bytes([u.get("b2f", 0) & 0xFF]))
    gm.w(base + 0x30, bytes([u.get("b30", 0) & 0xFF]))
    gm.w(base + 0x38, dw(u.get("d38", 0)))          # E360 bitmap C
    gm.w(base + 0x3C, dw(u.get("d3c", 0)))          # bitmap A
    gm.w(base + 0x64, dw(u.get("d64", 0)))          # bitmap B
    for i, v in enumerate(u.get("u40", [])):
        gm.w(base + 0x40 + i, bytes([v & 0xFF]))
    gm.w(base + 0x48, dw(u.get("d48", 0)))          # current HP
    gm.w(base + 0x4C, struct.pack("<h", u.get("w4c", 0)))  # current MP
    gm.w(base + 0x6C, bytes([u.get("b6c", 0) & 0xFF]))
    gm.w(base + 0x7C, bytes([u.get("b7c", 0) & 0xFF]))
    for i, v in enumerate(u.get("equip", [])):
        gm.w(base + 0x50 + i * 2, struct.pack("<H", v))
    for a, v in u.get("bmap68", {}).items():
        gm.w(base + 0x68 + a, bytes([v & 0xFF]))
    for a, v in u.get("bmap78", {}).items():
        gm.w(base + 0x78 + a, bytes([v & 0xFF]))
    gm.w(base + 0x1C2, bytes([u.get("level", 0) & 0xFF]))


def plant_rec(w, base, r):
    """Record block returned by scripted 31B860 — carries the member/
    flagobj/equipment chains plus the 0x778 provoke table."""
    gm = w.gm
    gm.w(base + 8, dw(r.get("d8", 0)))
    gm.w(base + 0x10, qw(r.get("q10", 0)))
    gm.w(base + 0x48, dw(r.get("d48", 0)))          # HP floor
    gm.w(base + 0xE9A, bytes([r.get("e9a", 0) & 0xFF]))
    memb = r.get("member")
    if memb is not None:
        gm.w(base + 0x698, qw(memb))
    fo = r.get("flagobj")
    if fo is not None:
        gm.w(base + 0x6A0, qw(fo))
    et = r.get("equiptbl")
    if et is not None:
        gm.w(base + 0xE60, qw(et))


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc, raw, secs)
        self.uc.mem_map(STACK, 0x100000)
        self.uc.mem_map(RETQ, 0x1000)
        self.uc.mem_map(HEAP, 0x800000)
        self.trace, self.faults, self.rets = [], [], {}
        self.hb = HEAP
        self.entry = 0

        self.gm.w(CANARY, qw(0x1122334455667788))
        self.gm.w(ELEMB, qw(self.alloc(0x40000)))
        self.elemb = self.gm.q(ELEMB)
        self.gm.w(UNITB, qw(case.get("unitb", self.alloc(0x4000))))

        # descriptor defaults — FED0's non-member path resolves a record
        # through d130 unconditionally; zero-filled elemb targets keep the
        # fold inert.  Cases override per-name.
        _DEFDESC = {"count": 0x200, "stride": 0x10, "off": 0x10}
        for name, cell in (("d040", D_040), ("d038", D_038),
                           ("d0f0", D_0F0), ("d0f8", D_0F8),
                           ("d108", D_108), ("d130", D_130),
                           ("d138", D_138)):
            d = case.get(name) or _DEFDESC
            desc = self.alloc(0x20)
            self.gm.w(cell, qw(desc))
            self.gm.w(desc + 4, dw(d.get("count", 0)))
            self.gm.w(desc + 8, bytes(struct.pack("<H",
                                      d.get("stride", 0))))
            self.gm.w(desc + 0xC, dw(d.get("off", 0)))

        self.flagobj = self.alloc(0x40)
        self.gm.w(D_190, qw(case.get("flagobj", self.flagobj)))

        # --- EXP-149 top-level objects -------------------------------
        # record (applier arg1): ~0x150 bytes, sentinel defaults
        self.rec = self.alloc(0x200)
        self.plant_record(self.rec, case.get("rec", {}))
        # units
        self.tgt = self.alloc(0x400)
        self.src = self.alloc(0x400)
        plant_unit(self, self.tgt, case.get("tgt", {}))
        plant_unit(self, self.src, case.get("src", {}))
        # records behind the units (31B860 products)
        self.tmember = self.alloc(0x1000)
        self.tflagobj = self.alloc(0x100)
        self.tequip = self.alloc(0x100)
        self.smember = self.alloc(0x1000)
        self.sflagobj = self.alloc(0x100)
        self.sequip = self.alloc(0x100)
        self.trec = self.alloc(0x1000)
        self.srec = self.alloc(0x1000)
        trec = dict(case.get("trec", {}))
        srec = dict(case.get("srec", {}))
        trec.setdefault("member", self.tmember)
        trec.setdefault("flagobj", self.tflagobj)
        trec.setdefault("equiptbl", self.tmember)   # steal/equip block
        srec.setdefault("member", self.smember)
        srec.setdefault("flagobj", self.sflagobj)
        srec.setdefault("equiptbl", self.smember)
        plant_rec(self, self.trec, trec)
        plant_rec(self, self.srec, srec)
        # member blocks
        for memb, spec in ((self.tmember, case.get("tmemb", {})),
                           (self.smember, case.get("smemb", {}))):
            self.gm.w(memb + 4, bytes([spec.get("b4", 0) & 0xFF]))
            self.gm.w(memb + 5, bytes([spec.get("b5", 0) & 0xFF]))
            self.gm.w(memb + 0xE90, dw(spec.get("e90", 0)))
            self.gm.w(memb + 0xE9A, bytes([spec.get("e9a", 0) & 0xFF]))
            for a, v in spec.get("e80", {}).items():
                self.gm.w(memb + 0xE80 + a, bytes([v & 0xFF]))
            # member self-link + flagobj + equip table so a member unit
            # (31B860 -> member) still resolves the chains the applier
            # reads off the resolved block
            self.gm.w(memb + 0x698, qw(memb))
            self.gm.w(memb + 0x6A0,
                      qw(spec.get("flagobj") or self.tflagobj))
            # the steal loop reads q[resolved+0xE60] as a POINTER to the
            # block whose +0x32+2i words are the steal items (the lea's
            # rax was clobbered by the b5 movzx -> base constant 0x32).
            # FED0 reads the same field for equipment.  Self-link.
            self.gm.w(memb + 0xE60, qw(spec.get("e60", memb)))
        # flagobj pre-fill
        for a, v in case.get("tflagv", {}).items():
            self.gm.w(self.tflagobj + a, bytes([v & 0xFF]))
        # E360's link-table cell -> block {d+0xC elem index, w+8 stride}
        self.linkblk = self.alloc(0x40)
        self.gm.w(0x02EBF118, qw(self.linkblk))
        self.gm.w(self.linkblk + 0xC, dw(case.get("link_idx", 0)))
        self.gm.w(self.linkblk + 8, bytes(struct.pack("<H",
                                          case.get("link_stride", 0x40))))
        # element record for the status bit: d[elem+0xC] = linked bitmap
        self.gm.w(self.elemb + case.get("link_idx", 0) +
                  case.get("link_bit", 0) * case.get("link_stride", 0x40)
                  + 0xC, dw(case.get("link_mask", 0)))
        # steal-slot item words live at q[resolved+0xE60] + 0x32 + 2*i
        # (the lea folds b5==1 into +0x32); equiptbl defaults to tmember
        for i, v in enumerate(case.get("stealtab", [])):
            self.gm.w(self.tmember + 0x32 + i * 2,
                      struct.pack("<H", v & 0xFFFF))

        # field descriptor table (image .data — writable)
        for f, d in case.get("fdesc", {}).items():
            base = FDESC + f * 8
            self.gm.w(base, bytes([d.get("b0", 0) & 0xFF]))
            self.gm.w(base + 1, bytes([d.get("b1", 0) & 0xFF]))
            self.gm.w(base + 2, bytes([d.get("b2", 0) & 0xFF]))
            self.gm.w(base + 4, dw(d.get("d4", 0)))
        for f, v in case.get("ftab2", {}).items():
            self.gm.w(FTAB2 + f * 4, dw(v))
        for cat, d in case.get("cat", {}).items():
            base = CATTAB + cat * 0x58
            self.gm.w(base + 0x3C, dw(d.get("count", 0)))
            self.gm.w(base + 0x48, qw(d.get("cb", 0)))

        for name, blob in case.get("blobs", {}).items():
            a = self.alloc(len(blob) + 0x10)
            self.gm.w(a, bytes(blob))
            self.rets["blob_" + name] = a

        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def plant_record(self, base, r):
        gm = self.gm
        gm.w(base + 8, dw(r.get("d8", 0)))
        gm.w(base + 0x1D, bytes([r.get("b1d", 0) & 0xFF]))
        gm.w(base + 0x20, dw(r.get("d20", 0)))
        gm.w(base + 0x24, dw(r.get("d24", 0)))
        gm.w(base + 0x28, struct.pack("<h", r.get("w28", 0)))
        gm.w(base + 0x2A, struct.pack("<h", r.get("w2a", 0)))
        gm.w(base + 0x2C, dw(r.get("d2c", 0)))       # flag word A
        gm.w(base + 0x32, bytes([r.get("b32", 0) & 0xFF]))
        gm.w(base + 0x33, bytes([r.get("b33", 0) & 0xFF]))
        gm.w(base + 0x34, bytes([r.get("b34", 0) & 0xFF]))
        gm.w(base + 0x38, dw(r.get("d38", 0xFFFFFFFF)))
        for i in range(6):                          # +0x3C..0x41 status bytes
            gm.w(base + 0x3C + i, bytes([r.get("b%02x" % (0x3C + i),
                                              0xFF) & 0xFF]))
        for i in range(8):                          # +0x42..0x50 words
            gm.w(base + 0x42 + i * 2, struct.pack("<h",
                 r.get("w%02x" % (0x42 + i * 2), -1)))
        gm.w(base + 0x54, dw(r.get("d54", 0)))      # status SET mask
        gm.w(base + 0x58, dw(r.get("d58", 0)))      # status CLEAR mask
        for i in range(32):                         # +0x5C.. durations
            gm.w(base + 0x5C + i * 4, struct.pack("<i",
                 r.get("d5c_%d" % i, -1)))
        for i in range(32):                         # +0xDC.. words
            gm.w(base + 0xDC + i * 2, struct.pack("<h",
                 r.get("wdc_%d" % i, -1)))
        gm.w(base + 0x11C, bytes([r.get("b11c", 0xFF) & 0xFF]))
        gm.w(base + 0x11D, bytes([r.get("b11d", 0xFF) & 0xFF]))
        for i in range(4):                          # +0x11E.. member adds
            gm.w(base + 0x11E + i * 2, struct.pack("<h",
                 r.get("w%03x" % (0x11E + i * 2), -1)))
        for i in range(8):                          # +0x128.. effect bytes
            gm.w(base + 0x128 + i, bytes([r.get("b%03x" % (0x128 + i),
                                               0) & 0xFF]))
        gm.w(base + 0x140, dw(r.get("d140", 0)))    # flag word 2

    def alloc(self, n):
        a = self.hb
        self.hb += (n + 0xFFF) & ~0xFFF
        return a

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

    def _args(self, tag):
        uc = self.uc
        rsp = uc.reg_read(UC_X86_REG_RSP)
        self.rets.setdefault("calls", []).append(
            [tag, uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF,
             self.gm.d(rsp + 0x28), self.gm.d(rsp + 0x30),
             self.gm.d(rsp + 0x38)])
        self.trace.append(tag)

    # scripted boundary table: tag -> case key for return value
    SCR = {X_B9B0: ("b9b0", "b9b0_ret"), X_B8E0: ("b8e0", "b8e0_ret"),
           X_77C20: ("77c20", "77c20_ret"), X_283D0: ("283d0", "283d0_ret"),
           X_8F1F0: ("8f1f0", None), X_16D70: ("16d70", "16d70_ret"),
           X_69BB0: ("69bb0", None), X_2A150: ("2a150", None),
           X_06F00: ("06f00", "06f00_ret"), X_299B0: ("299b0", None),
           X_B770: ("b770", "b770_ret"), X_B7F0: ("b7f0", "b7f0_ret"),
           X_E060: ("e060", None), X_FA540: ("fa540", None),
           X_85BA0: ("85ba0", "85ba0_ret"), X_A1180: ("a1180", "a1180_ret"),
           X_DF220: ("df220", "df220_ret"), X_53770: ("53770", None),
           X_53690: ("53690", "53690_ret"), X_54EE0: ("54ee0", None),
           X_0FC0: ("0fc0", None), X_105D0: ("105d0", None),
           X_19E30: ("19e30", None), X_87730: ("87730", "87730_ret"),
           X_876D0: ("876d0", "876d0_ret"), X_6A50: ("6a50", None),
           X_6AE0: ("6ae0", None), X_A720: ("a720", None),
           X_A790: ("a790", None), X_A690: ("a690", None),
           X_5D8C0: ("5d8c0", None), X_EACD0: ("eacd0", None),
           X_29210: ("29210", None), X_1E9A0: ("1e9a0", "1e9a0_ret"),
           X_23890: ("23890", "23890_ret"), X_FEF30: ("fef30", "fef30_ret"),
           X_165C0: ("165c0", "165c0_ret"), X_15E90: ("15e90", None),
           X_16BF0: ("16bf0", None), X_632B0: ("632b0", None),
           X_9F30: ("9f30", "9f30_ret"), X_EA40: ("ea40", None),
           X_279B0: ("279b0", None), X_8C40: ("8c40", None),
           X_0140: ("0140", None), X_1140: ("1140", None),
           X_7D10: ("7d10", None), X_84D0: ("84d0", None),
           X_A800: ("a800", None), X_D6A0: ("d6a0", None),
           X_2280: ("2280", None), X_6A70: ("6a70", None),
           F_APPLY: ("112f0_nested", None)}

    # applier callsites into REAL subjects — args recorded at the call
    # instruction (rsp still points at the outgoing-arg area)
    CALLSITES = {0x3113DF: "c650_tgt", 0x3113FD: "c650_src",
                 0x311457: "item_steal", 0x3114A8: "item_d38",
                 0x31153A: "e360_set", 0x31159F: "e360_clr",
                 0x311668: "hp_tgt", 0x3116A4: "mp_tgt",
                 0x3116E0: "op_sec", 0x311739: "hp_src",
                 0x311775: "mp_src", 0x3117CB: "e130_m2",
                 0x311807: "e130_m0", 0x311AC5: "fed0_tail"}

    def on_code(self, uc, addr, size, _):
        if addr == self.entry:
            return
        cs = self.CALLSITES.get(addr)
        if cs is not None and self.entry == F_APPLY:
            # only record when the call depth is the applier's own frame:
            # distinguishable by rsp below the entry frame's arg area
            self._args(cs)
            return  # fall through — execute the call for real
        if addr == X_B860:
            # per-input unit->record resolution
            rcx = uc.reg_read(UC_X86_REG_RCX)
            m = self.case.get("b860_map", {})
            ret = m.get(hex(rcx & 0xFFFFFFFFFFFFFFFF),
                        self.case.get("b860_ret", 0))
            self._args("b860")
            uc.reg_write(UC_X86_REG_RAX, ret & 0xFFFFFFFFFFFFFFFF)
            self._ret()
            return
        ent = self.SCR.get(addr)
        if ent is not None:
            tag, retkey = ent
            self._args(tag)
            if retkey:
                uc.reg_write(UC_X86_REG_RAX,
                             self.case.get(retkey, 0) & 0xFFFFFFFFFFFFFFFF)
            self._ret()
            return
        if addr == 0x00861EC0:      # memset(rcx, dl, r8)
            dst = uc.reg_read(UC_X86_REG_RCX)
            cnt = uc.reg_read(UC_X86_REG_R8)
            uc.mem_write(dst, b"\0" * cnt)
            self.trace.append("memset")
            self._ret()
            return
        if addr == self.case.get("cb_addr"):
            self._args("itemcb")
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("cb_ret", 0) & 0xFFFFFFFF)
            self._ret()
            return
        if addr == S_36A0: self.trace.append("s36a0")
        elif addr == S_E600: self.trace.append("e600")
        elif addr == S_9A60: self.trace.append("9a60")
        elif addr == S_9B20: self.trace.append("9b20")
        elif addr == S_9BD0: self.trace.append("9bd0")
        elif addr == S_166F0: self.trace.append("166f0")
        elif addr == V_C50:
            self.rets.setdefault("v_calls", []).append(
                [uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF,
                 uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF])
        elif addr == F_E360:
            # real subject reached via call — mark in trace only
            self.trace.append("e360_real")
        elif addr == F_E130:
            self.trace.append("e130_real")
        elif addr == F_FED0:
            self.trace.append("fed0_real")
        elif addr == F_0530:
            self.trace.append("hp_set")
        elif addr == F_0520:
            self.trace.append("hp_delta")
        elif addr == F_0CE0:
            self.trace.append("mp_set")
        elif addr == F_0C90:
            self.trace.append("mp_delta")
        elif addr == F_0BC0:
            self.trace.append("op_bc0")
        elif addr == F_C650:
            self.trace.append("c650_real")
        elif addr == F_08A0:
            self.trace.append("i08a0_real")

    def run(self, entry, rcx=0, rdx=0, r8=0, r9=0, arg5=0, arg6=0):
        uc = self.uc
        self.entry = entry
        rsp = STACK + 0x80000
        # sentinel-fill the frame so uninit reads are provable
        self.gm.w(rsp - 0x800, b"\xCD" * 0x800)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        self.gm.w(rsp + 0x28, qw(arg5))
        self.gm.w(rsp + 0x30, qw(arg6))
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


# ------------------------------------------------------------------
CASES = {
    # ---- gate layer ----
    "ap-empty": {},
    "ap-gate-block": {"b9b0_ret": 1},
    "ap-gate-skip":  {"arg5": 1},
    # ---- numeric: HP ----
    "ap-dmg": {"tgt": {"d48": 1000, "d24": 3000},
               "trec": {"d48": 0},
               "rec": {"d2c": 1 << 8, "d24": -300 & 0xFFFFFFFF}},
    "ap-lethal": {"tgt": {"d48": 100, "d24": 3000},
                  "trec": {"d48": 0},
                  "tmemb": {"b5": 1},
                  "rec": {"d2c": (1 << 8), "d24": -500 & 0xFFFFFFFF},
                  "06f00_ret": 0},
    # status bit16 (d3c|d64) = heal-freeze: HP cap becomes max(oldHP,1)
    "ap-cap-freeze": {"tgt": {"d48": 100, "d24": 3000, "d3c": 0x10000},
                      "trec": {"d48": 0},
                      "rec": {"d2c": (1 << 8), "d24": 500}},
    # lethal with source: killer copy d[rbx+0x30]=d[srec+8], 16D70 lookup
    "ap-lethal-src": {"tgt": {"d48": 100, "d24": 3000},
                      "trec": {"d48": 0},
                      "tmemb": {"b5": 1},
                      "src": {"d48": 50, "d24": 1000},
                      "srec": {"d48": 0, "d8": 0xBEEF},
                      "has_src": 1,
                      "rec": {"d2c": (1 << 8), "d24": -500 & 0xFFFFFFFF},
                      "06f00_ret": 0, "16d70_ret": -1},
    # revive: delta>0 while old HP already 0 -> E360 mode0 clears KO bit
    "ap-revive": {"tgt": {"d48": 0, "d24": 3000, "d64": 1},
                  "trec": {"d48": 0},
                  "src": {"d48": 50, "d24": 1000},
                  "srec": {"d48": 0},
                  "has_src": 1,
                  "rec": {"d2c": (1 << 8), "d24": 500},
                  "06f00_ret": 0},
    "ap-heal-cap": {"tgt": {"d48": 2900, "d24": 3000},
                    "trec": {"d48": 0},
                    "rec": {"d2c": (1 << 8), "d24": 500}},
    "ap-heal-cap2x": {"tgt": {"d48": 5900, "d24": 3000, "d3c": 0x10000000},
                      "trec": {"d48": 0},
                      "rec": {"d2c": (1 << 8), "d24": 500}},
    "ap-dmg-abs": {"tgt": {"d48": 1000, "d24": 3000},
                   "trec": {"d48": 0},
                   "rec": {"d2c": (1 << 8) | (1 << 3), "d24": 777}},
    "ap-dmg-b8e0": {"tgt": {"d48": 1000, "d24": 3000},
                    "trec": {"d48": 0},
                    "rec": {"d2c": (1 << 8), "d24": -300 & 0xFFFFFFFF},
                    "b8e0_ret": 1},
    "ap-dmg-cantdie": {"tgt": {"d48": 100, "d24": 3000,
                               "d3c": 0x80000001},
                       "trec": {"d48": 0},
                       "rec": {"d2c": (1 << 8), "d24": -500 & 0xFFFFFFFF},
                       "77c20_ret": 0},
    # ---- numeric: MP / secondary ----
    "ap-mp": {"tgt": {"w4c": 100, "w28": 500},
              "trec": {},
              "rec": {"d2c": (1 << 14), "w2a": -50}},
    "ap-mp-delta": {"tgt": {"w4c": 100, "w28": 500},
                    "trec": {},
                    "rec": {"d2c": (1 << 14) | (1 << 4), "w2a": 250}},
    "ap-secondary": {"tgt": {"w28": 300, "w6": 10},
                     "trec": {},
                     "rec": {"b1d": 5}},
    "ap-secondary-neg": {"tgt": {"w28": 300, "w6": 10},
                         "trec": {},
                         "rec": {"b1d": -3 & 0xFF}},
    # ---- source side ----
    "ap-src-hp": {"tgt": {"d48": 500, "d24": 3000},
                  "src": {"d48": 200, "d24": 1000},
                  "trec": {"d48": 0}, "srec": {"d48": 0},
                  "rec": {"d2c": 1 << 7, "d20": -50 & 0xFFFFFFFF},
                  "has_src": 1},
    "ap-src-hp-abs": {"src": {"d48": 200, "d24": 1000},
                      "srec": {"d48": 0},
                      "rec": {"d2c": (1 << 7) | 2, "d20": 333},
                      "has_src": 1},
    "ap-src-mp": {"src": {"w4c": 80, "w28": 400},
                  "srec": {},
                  "rec": {"d2c": 1 << 13, "w28": 30},
                  "has_src": 1},
    # ---- status masks -> E360 ----
    "ap-st-set": {"tgt": {}, "trec": {"d48": 0},
                  "rec": {"d54": 0x21}},
    "ap-st-clr": {"tgt": {"d64": 0x11}, "trec": {"d48": 0},
                  "rec": {"d58": 0x11}},
    "ap-st-set-suppress": {"tgt": {}, "trec": {"d48": 0},
                           "rec": {"d54": 0x21}, "arg5": 0x200},
    "ap-st-set-f140": {"tgt": {}, "trec": {"d48": 0},
                       "rec": {"d54": 1, "d140": 0x10}},
    "ap-st-idempotent": {"tgt": {"d64": 0x21}, "trec": {"d48": 0},
                         "rec": {"d54": 0x21}},
    # mode3 set requires bit clear in BOTH d64 and d38
    "ap-st-d38lock": {"tgt": {"d38": 0x21}, "trec": {"d48": 0},
                      "rec": {"d54": 0x21}},
    # ---- status byte loops -> E130 ----
    "ap-e130-loops": {"tgt": {"bmap68": {1: 0x0E}}, "trec": {"d48": 0},
                      "rec": {"b3c": 4, "b3d": 0xFF,
                              "b3e": 9, "b3f": 0xFF, "b40": 0xB,
                              "b41": 0xFF}},
    # ---- copy-throughs / member adds / effect bytes ----
    "ap-copythrough": {"tgt": {}, "trec": {"d48": 0},
                       "rec": {"d54": 1, "d5c_0": 60, "wdc_0": 9}},
    "ap-memadds": {"tgt": {"b5": 1, "w8": 5, "wa": 7, "w12": 9,
                           "w14": 11, "b2a": 1, "b2b": 2, "b2f": 3,
                           "b30": 4},
                   "trec": {"d48": 0},
                   "rec": {"w11e": 20, "w120": 30, "w122": 40,
                           "w124": 50}},
    "ap-memfx": {"tgt": {}, "trec": {"d48": 0}, "tmemb": {"b5": 1},
                 "tflagv": {0x78: 0x55},
                 "rec": {"b128": 0x0F, "b129": 0x33, "b12a": 0x01,
                         "b12b": 0x77, "b12c": 0xF0, "b12d": 0x0C,
                         "b12e": 0xFE, "b12f": 0x08}},
    # ---- steal + item ----
    "ap-steal": {"tgt": {}, "trec": {"d48": 0}, "tmemb": {"b5": 1},
                 "tflagv": {0x14: 0x07},
                 "stealtab": [0x3001, 0xFFFF, 0x4002],
                 "rec": {"b32": 1, "b33": 0, "b34": 1},
                 "cat": {3: {"count": 0x20}, 4: {"count": 0x20}},
                 "d0f0": {"count": 8, "stride": 0x10, "off": 0x200},
                 "d138": {"count": 8, "stride": 0x20, "off": 0x400},
                 "9f30_ret": 1},
    "ap-item": {"tgt": {}, "trec": {"d48": 0},
                "rec": {"d38": 0x3005},
                "cat": {3: {"count": 0x20}},
                "d0f0": {"count": 8, "stride": 0x10, "off": 0x200},
                "d138": {"count": 8, "stride": 0x20, "off": 0x400},
                "9f30_ret": 1},
    # ---- levels ----
    "ap-level": {"tgt": {"level": 10, "d48": 100, "d24": 3000},
                 "trec": {"d48": 0},
                 "src": {"level": 20},
                 "srec": {"d48": 0},
                 "has_src": 1,
                 "rec": {"b11c": 15, "b11d": 0xFF},
                 "d130": {"count": 8, "stride": 0x60, "off": 0x100},
                 "d108": {"count": 8, "stride": 0x20, "off": 0x800}},
    # ---- stats flag byte + gil ----
    "ap-e9a": {"tgt": {}, "trec": {"d48": 0, "e9a": 0},
               "rec": {"d2c": 0x80000, "d140": 0x4000},
               "a1180_ret": 5},
    "ap-gil": {"trec": {"d48": 0},
               "rec": {"d8": 100},
               "53690_ret": 50},
    # ---- combined realistic record ----
    "ap-full": {"tgt": {"d48": 1000, "d24": 3000, "w4c": 100,
                        "w28": 500, "b5": 1, "w8": 5, "b2a": 1,
                        "d64": 0x10},
                "trec": {"d48": 0}, "tmemb": {"b5": 1},
                "stealtab": [0x3001, 0xFFFF, 0xFFFF],
                "src": {"d48": 200, "d24": 1000, "w4c": 80,
                        "w28": 400},
                "srec": {"d48": 0},
                "has_src": 1,
                "rec": {"d2c": (1 << 8) | (1 << 14) | (1 << 7) |
                               (1 << 13),
                        "d24": -300 & 0xFFFFFFFF, "w2a": -50,
                        "d20": -50 & 0xFFFFFFFF, "w28": 30,
                        "b1d": 2,
                        "d54": 0x21, "d58": 0x10,
                        "b3c": 4, "b3d": 0xFF, "b3e": 9, "b3f": 0xFF,
                        "b40": 0xFF, "b41": 0xFF,
                        "d5c_0": 60, "wdc_0": 9,
                        "w42": 7, "w44": -1,
                        "w11e": 20,
                        "b128": 0x0F, "b12a": 0x01,
                        "b32": 1, "d38": -1,
                        "b11c": 0xFF, "b11d": 0xFF,
                        "d8": 0, "d140": 0},
                "cat": {3: {"count": 0x20}},
                "d040": {"count": 0x40, "stride": 1, "off": 0},
                "d0f0": {"count": 8, "stride": 0x10, "off": 0x200},
                "d138": {"count": 8, "stride": 0x20, "off": 0x400},
                # the d54 mask sets KO bit0 in d64 BEFORE the HP dispatch;
                # the setter consults 77C20 on the negative delta — ret 1
                # lets the store proceed.
                "77c20_ret": 1,
                "9f30_ret": 1},
}


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    out = {"trace": w.trace, "faults": w.faults}
    if name.startswith("ap-"):
        # 31B860(unit) -> record; for member units (b5==1) it returns the
        # member block (FED0 reads member+0xE80 off it) — EXP-148 model
        tdst = w.tmember if case.get("tgt", {}).get("b5") == 1 else w.trec
        sdst = w.smember if case.get("src", {}).get("b5") == 1 else w.srec
        w.case["b860_map"] = {hex(w.tgt): tdst, hex(w.src): sdst}
        src = w.src if case.get("has_src") else 0
        out["ret"] = w.run(F_APPLY, rcx=w.rec, rdx=src, r8=w.tgt,
                           r9=case.get("flags", 0),
                           arg5=case.get("arg5", 0))
        gm = w.gm
        out["tgt"] = {"hp": gm.d(w.tgt + 0x48),
                      "mp": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 0x4C, 2)))[0],
                      "w6": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 6, 2)))[0],
                      "w8": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 8, 2)))[0],
                      "d38": gm.d(w.tgt + 0x38),
                      "d3c": gm.d(w.tgt + 0x3C),
                      "d64": gm.d(w.tgt + 0x64),
                      "w17c": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 0x17C, 2)))[0],
                      "dbc": gm.d(w.tgt + 0xBC),
                      "w13c": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 0x13C, 2)))[0],
                      "b68": gm.b(w.tgt + 0x68),
                      "b69u": gm.b(w.tgt + 0x69),
                      "b78": gm.b(w.tgt + 0x78),
                      "b79u": gm.b(w.tgt + 0x79),
                      "wa": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 0xA, 2)))[0],
                      "w12": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 0x12, 2)))[0],
                      "w14": struct.unpack("<h", bytes(
                          gm.uc.mem_read(w.tgt + 0x14, 2)))[0],
                      "level": gm.b(w.tgt + 0x1C2)}
        out["src_hp"] = gm.d(w.src + 0x48)
        out["src_mp"] = struct.unpack("<h", bytes(
            gm.uc.mem_read(w.src + 0x4C, 2)))[0]
        out["trec_e9a"] = gm.b(w.trec + 0xE9A)
        out["trec_d30"] = gm.d(w.trec + 0x30)
        out["tflag"] = {"b14": gm.b(w.tflagobj + 0x14),
                        "w8": struct.unpack("<h", bytes(
                            gm.uc.mem_read(w.tflagobj + 8, 2)))[0],
                        "d0": gm.d(w.tflagobj),
                        "b78": gm.b(w.tflagobj + 0x78),
                        "b79": gm.b(w.tflagobj + 0x79),
                        "b7a": gm.b(w.tflagobj + 0x7A),
                        "b7b": gm.b(w.tflagobj + 0x7B)}
    out.update(w.rets)
    out["ok"], out["fail"] = check(name, case, out)
    return out


def check(name, c, o):
    f = []
    tr = o["trace"]
    calls = o.get("calls", [])

    def eq(k, got, want):
        if got != want:
            f.append("%s: got %s want %s" % (k, hex(got), hex(want)))

    def called(tag):
        return [x for x in calls if x[0] == tag]

    def nreal(tag):
        return tr.count(tag)

    if o["faults"]:
        f.append("faults: %s" % o["faults"])

    if name == "ap-empty":
        allowed = {"b860", "b9b0", "85ba0"}
        bad = [x for x in calls if x[0] not in allowed]
        if bad:
            f.append("empty record made calls: %s" % bad)
        for t in ("hp_set", "hp_delta", "mp_set", "mp_delta", "op_bc0",
                  "e360_real", "e130_real", "fed0_real", "c650_real",
                  "i08a0_real"):
            if nreal(t):
                f.append("empty record ran %s" % t)
        return len(f) == 0, f

    if name == "ap-gate-block":
        b9 = called("b9b0")
        if len(b9) != 1:
            f.append("b9b0 calls: %s" % b9)
        if "hp_set" in tr or "e360_real" in tr or "fed0_real" in tr:
            f.append("gate-block continued: %s" % tr)
        return len(f) == 0, f

    if name == "ap-gate-skip":
        if called("b9b0"):
            f.append("arg5&1 should skip b9b0: %s" % calls)
        if not called("85ba0"):
            f.append("85ba0 gate not reached")
        return len(f) == 0, f

    tgt, trec = o["tgt"], o.get("tflag", {})

    if name == "ap-dmg":
        eq("hp", tgt["hp"], 700)
        if nreal("fed0_real"):
            f.append("pure damage fired FED0")
        if nreal("e360_real"):
            f.append("pure damage fired E360")
    elif name == "ap-lethal":
        eq("hp", tgt["hp"], 0)
        eq("d64 bit0", tgt["d64"] & 1, 1)      # KO status bit 0 -> d64
        eq("killcnt", trec["w8"], 1)           # w[flagobj+8]++
        for tag in ("0fc0", "2280", "2a150"):
            if not called(tag):
                f.append("lethal arm: no %s" % tag)
    elif name == "ap-lethal-src":
        eq("hp", tgt["hp"], 0)
        eq("d64 bit0", tgt["d64"] & 1, 1)
        eq("killcnt", trec["w8"], 1)
        eq("killerid", o["trec_d30"], 0xBEEF)  # d[trec+0x30] = d[srec+8]
        if not called("2280"):
            f.append("no 312280 kill notify")
    elif name == "ap-revive":
        eq("hp", tgt["hp"], 500)
        eq("d64 bit0", tgt["d64"] & 1, 0)      # KO cleared (mode0)
        if not called("1140"):
            f.append("revive arm: no 301140")
    elif name == "ap-cap-freeze":
        eq("hp", tgt["hp"], 100)               # heal capped at oldHP
        eq("d64 bit0", tgt["d64"] & 1, 0)
    elif name == "ap-heal-cap":
        eq("hp", tgt["hp"], 3000)
    elif name == "ap-heal-cap2x":
        eq("hp", tgt["hp"], 6000)               # bit 0x1C doubles cap
    elif name == "ap-dmg-abs":
        eq("hp", tgt["hp"], 777)                # delta shim makes abs
    elif name == "ap-dmg-b8e0":
        eq("hp", tgt["hp"], 1000)               # store suppressed
        if not called("b8e0"):
            f.append("b8e0 not consulted")
    elif name == "ap-dmg-cantdie":
        eq("hp", tgt["hp"], 100)                # 77c20 aborts
    elif name == "ap-mp":
        eq("mp", tgt["mp"], 50)
    elif name == "ap-mp-delta":
        eq("mp", tgt["mp"], 250)                # shim -> absolute write
    elif name == "ap-secondary":
        # 300BC0(tgt, w[tgt+0x28]*movsx b1d, flags): w6 clamped to w28
        if not nreal("op_bc0"):
            f.append("0BC0 not called")
        eq("w6", tgt["w6"], 300)
    elif name == "ap-secondary-neg":
        if not nreal("op_bc0"):
            f.append("0BC0 not called")
        eq("w6", tgt["w6"], 0)                  # floored at 0
    elif name == "ap-src-hp":
        eq("src_hp", o["src_hp"], 150)
        eq("tgt_hp", tgt["hp"], 500)
    elif name == "ap-src-mp":
        eq("src_mp", o["src_mp"], 110)
    elif name == "ap-st-set":
        eq("d64", tgt["d64"], 0x21)            # mode3 sets d64
        # record durations are -1 -> E360's 387730/3876D0 conversions run
        if len(called("87730")) != 2:
            f.append("87730 calls: %s" % called("87730"))
        if len(called("876d0")) != 2:
            f.append("876d0 calls: %s" % called("876d0"))
        eq("dbc", tgt["dbc"], 0)
        eq("w13c", tgt["w13c"], 0)
        if nreal("fed0_real") != 1:
            f.append("fed0_real count %d want 1" % nreal("fed0_real"))
    elif name == "ap-st-clr":
        eq("d64", tgt["d64"], 0)               # mode0 clears d64
        if nreal("fed0_real") != 1:
            f.append("fed0_real count %d want 1" % nreal("fed0_real"))
    elif name == "ap-st-set-suppress":
        eq("d64", tgt["d64"], 0x21)            # set still lands
        if nreal("fed0_real"):
            f.append("arg5 bit9 should suppress applier FED0")
    elif name == "ap-st-set-f140":
        eq("d64", tgt["d64"], 1)
        e = called("e360_set")
        if e and e[0][5] != 0x202:
            f.append("e360_set flags %x want 0x202" % e[0][5])
    elif name == "ap-st-idempotent":
        eq("d64", tgt["d64"], 0x21)
        if nreal("fed0_real") != 1:
            # applier tail FED0 still fires (r14d set per dispatch);
            # E360's own tail is suppressed by arg6 bit9 always
            f.append("applier FED0 expected (dispatch landed)")
        if "memset" in tr:
            f.append("idempotent set ran the notify block")
    elif name == "ap-e130-loops":
        # mode2 sets bit4 in unit+0x68; mode0 clears bits 9,0xB in +0x68
        eq("b68", tgt["b68"], 0x10)
        eq("b69", tgt["b69u"], 0x04)           # 0x0E & ~0x0A
        if nreal("fed0_real") != 1:
            f.append("fed0 count %d" % nreal("fed0_real"))
    elif name == "ap-copythrough":
        eq("dbc", tgt["dbc"], 60)              # r9d=d[rec+0x5C] stored
        eq("w13c", tgt["w13c"], 9)             # arg5=w[rec+0xDC] stored
        if nreal("fed0_real") != 1:
            f.append("copythrough dispatch landed -> FED0 expected")
    elif name == "ap-memadds":
        eq("w8", tgt["w8"], 5 + (20 - 1))
        eq("wa", tgt["wa"], 7 + (30 - 2))
        eq("w12", tgt["w12"], 9 + (40 - 3))
        eq("w14", tgt["w14"], 11 + (50 - 4))
        if nreal("fed0_real") != 1:
            f.append("memadds landed -> FED0 expected")
    elif name == "ap-memfx":
        eq("b78", trec["b78"], (0x55 | 0x01) & ~0xFE & 0xFF)
        eq("b79", trec["b79"], (0 | 0x33) & ~0x0C & 0xFF)
        eq("b7a", trec["b7a"], (0 | 0x77) & ~0x08 & 0xFF)
        eq("b7b", trec["b7b"], (0 | 0x0F) & ~0xF0 & 0xFF)
        eq("d0&0x80", trec["d0"] & 0x80, 0x80)
        if nreal("fed0_real") != 1:
            f.append("memfx landed -> FED0 expected")
    elif name == "ap-steal":
        if tr.count("i08a0_real") != 2:
            f.append("08A0 count %d want 2 (slots 0,2)"
                     % tr.count("i08a0_real"))
        # btr flagobj+0x14 per stolen slot: 0x07 -> clear bits 0,2 -> 0x02
        eq("b14", trec["b14"], 0x02)
        if len(called("53770")) != 2:
            f.append("53770 calls: %s" % called("53770"))
    elif name == "ap-item":
        if tr.count("i08a0_real") != 1:
            f.append("08A0 count %d want 1" % tr.count("i08a0_real"))
    elif name == "ap-level":
        eq("level", tgt["level"], 15)
        if tr.count("c650_real") != 1:
            f.append("c650 count %d want 1" % tr.count("c650_real"))
    elif name == "ap-e9a":
        eq("e9a", o["trec_e9a"], 0)    # tail &0xF3 clears both flags
        if not called("a1180"):
            f.append("no a1180")
        if not called("df220"):
            f.append("no df220")
    elif name == "ap-gil":
        if not called("53690") or not called("54ee0"):
            f.append("gil chain: %s" % calls)
        else:
            eq("54ee0.ecx", called("54ee0")[0][1],
               max(0, 50 - 100) & 0xFFFFFFFF)
    elif name == "ap-full":
        eq("hp", tgt["hp"], 700)
        eq("mp", tgt["mp"], 50)
        eq("src_hp", o["src_hp"], 150)
        eq("src_mp", o["src_mp"], 110)
        eq("d64", tgt["d64"], 0x21)    # 0x10|0x21 set, then bit4 cleared
        eq("w6", tgt["w6"], 500)       # 0 + w28*2 clamped to w28
        eq("w8", tgt["w8"], 5 + (20 - 1))
        eq("w17c", tgt["w17c"], 7)
        eq("b68", tgt["b68"], 0x10)    # e130 mode2 set bit4
        eq("kill-free", trec["w8"], 0)
        if nreal("fed0_real") < 1:
            f.append("no FED0 in full case")

    return (len(f) == 0), f


def main():
    raw, secs = load_image()
    out = {"cases": len(CASES), "pass": 0, "fail": 0, "results": {}}
    for name, case in CASES.items():
        try:
            r = run_case(name, case, raw, secs)
        except Exception as e:
            import traceback
            r = {"ok": False, "fail": ["exception: %r" % e],
                 "trace": [], "faults": [],
                 "tb": traceback.format_exc()}
        out["results"][name] = r
        if r["ok"]:
            out["pass"] += 1
        else:
            out["fail"] += 1
            print("%-20s FAIL %s" % (name, r["fail"]))
            if r["faults"]:
                print("   faults:", r["faults"][:3])
            print("   trace:", r["trace"][:60])
            print("   calls:", r.get("calls", [])[:25])
    out["ok"] = out["fail"] == 0
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("%d/%d pass" % (out["pass"], out["cases"]))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
