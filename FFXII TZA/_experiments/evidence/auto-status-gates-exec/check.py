#!/usr/bin/env python3
"""EXP-100 auto-status-gates-exec - BattleStats_RebuildAutoStatuses
0030FED0 executed with its three GATE oracles real: the validity
dispatcher 00322C50 (arm 6: equipment-id range over [02EBF0F8]+4), the
equipment-kind classifier 0031E9A0 -> 0031E9F0 (row[+9] -> class -> gate
{0,1,2,3}), and the licence gate 00323890 -> 003241D0 (row[+5] -> class
-> gate {0,1,2,3,-1}). The pilot (diff_auto_status.py) fed oracle
answers; here the gates run from shipped bytes, so which equipment types
and licence rows can contribute is measured, not asserted.

    0030FED0  subject   REAL - kind byte rec+5; kind0: def-row masks
              row+0x50/+0x54 -> acc bits 0..63; all kinds: 5 equip slots
              u16[rec+0x50+2k] -> 00322C50(6,id) -> row = resolve(
              [equip+0xC]) + (id-0x1000)*u16[equip+8] -> 0031E9A0(row)
              ==3 -> bts acc[u8[row+0x1A]] (0xFF skips); licence walk
              id=0..360, owned bit rec+0x194+id/8 bit id%8 -> row ->
              u8[row+5] -> 00323890 ==2 -> 8 grants u16[row+8+2k]
              !=0xFFFF -> bts. diff vs prior rec+0x78 -> APPLY(rec,bit,
              0,flags|0x202,3 add / 1 rem). NOTIFY(rec,0,0) once.
              kind1: FIND->unit; u32[unit+0xE90] bits 0..31 ->
              CASCADE(rec,0,bit,0,0,flags,5); spawn=[unit+0x6A0]:
              byte[0]&0x80 -> copy spawn+0x78..0x7C -> rec+0x40..44,
              else the other way. clamps: presence=[rec+0x64]|[+0x3C];
              bit16 freeze; bit28 doubles [rec+0x24]; hp=min(hp,cap)
              unless frozen; mp/+0x06 caps = (byte[0x6C]<0 or
              byte[0x7C]<0) ? 0 : sx16(rec+0x28) [* byte[0x37] for +0x06
              when nonzero]. TAIL(rec,flags|0x202). ret 0.
    0020E600  resolver  REAL - zero-extended base+encoded add.
    00322C50  validity  REAL - ecx-1<=0x1F arm dispatch; arm6:
              tab=[02EBF0F8]; ret id in [0x1000, 0x1000+[tab+4]).
    0031E9A0  eq gate   REAL - 0031E9F0 class: <=0->0, 1..5->1, 6->2,
              7..9->3.
    0031E9F0  eq class  REAL - byte[rcx+9] <=0x1A -> class via byte
              table 0031EA74 + jump table 0031EA50; else 0.
    00323890  lic gate  REAL - class-0x15 <=9 -> map {0,1,2,3}; else -1.
    003241D0  lic class REAL - (ecx-1)<=0x1D -> class via byte table
              00324260 + jump table 00324234; else 0.
    00808C40  cookie    REAL - prologue/epilogue both run.
    0016D6A0  CFG stub  REAL - ret 0 (not reached on this path).

    Scripted oracles (disclosed boundaries, args captured):
    0031B860 FIND    - record->unit; returns planted unit or 0.
    0030E130 APPLY   - per changed bit; mode 3 add / 1 remove.
    0030E360 CASCADE - per unit+0xE90 bit, mode 5.
    002FEF30 NOTIFY  - once per run.
    0030E060 TAIL    - final recompute entry point.

Trace tokens: F FIND, V<arm>:<id>=<r> validity, E<t9>=<g> eq gate,
L<b5>=<g> lic gate, A<bit>+<3|1> apply, C<bit> cascade, N notify,
T<flags> tail. Observables: trace + record dump (hp +0x48, mp +0x4C,
w6 +0x06, exchange bytes rec+0x40..44 / spawn+0x78..0x7C, prior
+0x78[16]).

NOT EXERCISED (disclosed): FIND/APPLY/CASCADE/NOTIFY/TAIL bodies, the
callers, the authored table file loaders, no live process.
"""
import ctypes, hashlib, json, struct, sys
from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
IMG32  = 0x50000000          # authored-data arena BASE_AT points at
                             # (outside the mapped image extent)
REC    = HEAP + 0x000000     # stats record (rbx)
UNIT   = HEAP + 0x100000     # battle unit (FIND result)
SPAWN  = HEAP + 0x200000     # spawn record ([unit+0x6A0])

SUBJ    = 0x0030FED0
FIND    = 0x0031B860
VALID   = 0x00322C50
EQGATE  = 0x0031E9A0
EQCLASS = 0x0031E9F0
LICGATE = 0x00323890
LICCLAS = 0x003241D0
APPLY   = 0x0030E130
CASCADE = 0x0030E360
NOTIFY  = 0x002FEF30
TAIL    = 0x0030E060
COOKIE  = 0x00808C40
RESOLVE = 0x0020E600

BASE_AT     = 0x01F83530
DEF_SLOT    = 0x02EBF130     # -> def table header
EQUIP_SLOT  = 0x02EBF0F8     # -> equipment table header (arm 6 source)
LIC_SLOT    = 0x02EBF038     # -> licence table header

STUBS = (FIND, APPLY, CASCADE, NOTIFY, TAIL)
HOOKS = {FIND: "F", VALID: "V", EQGATE: "E", EQCLASS: "e", LICGATE: "L",
         LICCLAS: "l", APPLY: "A", CASCADE: "C", NOTIFY: "N", TAIL: "T",
         RESOLVE: "R", COOKIE: "k"}


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)


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


# ---- gate models (algorithm level; tables read from the shipped image) -------

def read_va(raw, secs, va, n):
    r = va - 0x120000
    for sva, vs, ra, rs in secs:
        if sva <= r < sva + rs:
            return raw[ra + r - sva: ra + r - sva + n]
    return None


class GateModel:
    """Semantic model of the three real gates, reading the shipped tables."""

    def __init__(self, raw, secs):
        self.eq_bt = read_va(raw, secs, 0x31EA74, 0x1B)
        self.eq_jt = read_va(raw, secs, 0x31EA50, 9 * 4)
        self.lic_bt = read_va(raw, secs, 0x324260, 0x1E)
        self.lic_jt = read_va(raw, secs, 0x324234, 11 * 4)
        self.gate_jt = read_va(raw, secs, 0x3238E4, 10 * 4)
        self.eq_cls = {0x31EA14 + 6 * i: i + 1 for i in range(9)}
        self.lic_cls = {0x3241F5 + 6 * i: 0x15 + i for i in range(10)}
        self.gate_arm = {0x3238B6: 0, 0x3238BD: 1, 0x3238C7: 2,
                         0x3238D1: 3}

    def eq_class(self, b):
        if b > 0x1A:
            return 0
        j = self.eq_bt[b]
        return self.eq_cls.get(struct.unpack_from("<i", self.eq_jt,
                                                  j * 4)[0] + 0x120000, 0)

    def eq_gate(self, b):
        c = self.eq_class(b)
        if c <= 0: return 0
        if c <= 5: return 1
        if c == 6: return 2
        if c <= 9: return 3
        return 0

    def lic_class(self, b):
        c = (b - 1) & 0xFFFFFFFF
        if c > 0x1D:
            return 0
        j = self.lic_bt[c]
        return self.lic_cls.get(struct.unpack_from("<i", self.lic_jt,
                                                   j * 4)[0] + 0x120000, 0)

    def lic_gate(self, b):
        a = self.lic_class(b) - 0x15
        if a < 0 or a > 9:
            return -1
        return self.gate_arm.get(struct.unpack_from("<i", self.gate_jt,
                                                    a * 4)[0] + 0x120000, -1)

    def valid6(self, ident, count, tab_present):
        hi = (count + 0x1000) if tab_present else 0x1000
        return 1 if (0x1000 <= ident <= hi - 1) else 0


# ---- guest world --------------------------------------------------------------

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
        self.gm.map(0, 0x1000)          # null-row page: reads as zeros
        for a, s in [(HEAP, 0x400000), (IMG32, 0x20000),
                     (STACK, 0x100000), (RETQ, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")

        # authored-data base + three registry slots -> headers in IMG32
        gm.w(BASE_AT, qw(IMG32))
        for slot, hdr in ((DEF_SLOT, case.get("def_hdr")),
                          (EQUIP_SLOT, case.get("equip_hdr")),
                          (LIC_SLOT, case.get("lic_hdr"))):
            gm.w(slot, qw(0 if hdr is None else IMG32 + hdr))
        # headers: +4 count dword, +8 stride word, +0xC encoded row offset
        for hdr, stride, rows, count in (
                (case.get("def_hdr"), 0x40, 0x1000, 0),
                (case.get("equip_hdr"), 0x20, 0x2000,
                 case.get("equip_count", 0)),
                (case.get("lic_hdr"), 0x20, 0x4000, 0)):
            if hdr is not None:
                gm.w(IMG32 + hdr + 4, dw(count))
                gm.w(IMG32 + hdr + 8, struct.pack("<H", stride))
                gm.w(IMG32 + hdr + 0xC, dw(rows))

        # record
        gm.w(REC + 4, bytes([case.get("row_idx", 0) & 0xFF]))
        gm.w(REC + 5, bytes([case.get("kind", 0) & 0xFF]))
        gm.w(REC + 6, struct.pack("<h", case.get("w6", 0)))
        gm.w(REC + 0x24, dw(case.get("maxhp", 0)))
        gm.w(REC + 0x28, struct.pack("<h", case.get("stat28", 0)))
        gm.w(REC + 0x37, bytes([case.get("mult37", 0) & 0xFF]))
        gm.w(REC + 0x3C, dw(case.get("pres3c", 0)))
        gm.w(REC + 0x40, bytes(case.get("rec40", [0] * 5)))
        gm.w(REC + 0x48, struct.pack("<i", case.get("hp", 0)))
        gm.w(REC + 0x4C, struct.pack("<h", case.get("mp", 0)))
        gm.w(REC + 0x50, b"".join(struct.pack("<H", i & 0xFFFF)
                                 for i in case.get("equip_ids",
                                                  [0] * 5)))
        gm.w(REC + 0x64, dw(case.get("pres64", 0)))
        gm.w(REC + 0x6C, bytes([case.get("g6c", 0) & 0xFF]))
        gm.w(REC + 0x78, bytes(case.get("prior", [0] * 16)))
        gm.w(REC + 0x7C, bytes([case.get("g7c", 0) & 0xFF]))
        owned = bytearray(46)
        for i in case.get("lic_owned", []):
            owned[i // 8] |= 1 << (i % 8)
        gm.w(REC + 0x194, bytes(owned))

        # definition row: rows at +0x1000 stride 0x40; masks at
        # row+0x50 (acc bits 0..31) and row+0x54 (bits 32..63)
        if case.get("def_hdr") is not None:
            drow = 0x1000 + case.get("row_idx", 0) * 0x40
            gm.w(IMG32 + drow + 0x50, dw(case.get("def_m0", 0)))
            gm.w(IMG32 + drow + 0x54, dw(case.get("def_m1", 0)))

        # equipment rows: row = equip_rows + (id-0x1000)*0x20; +9 type,
        # +0x1A status byte
        for ident, t9 in case.get("eq_t9", {}).items():
            row = 0x2000 + (ident - 0x1000) * 0x20
            gm.w(IMG32 + row + 9, bytes([t9 & 0xFF]))
            gm.w(IMG32 + row + 0x1A,
                 bytes([case.get("eq_st", {}).get(ident, 0xFF) & 0xFF]))
        # licence rows: row = lic_rows + id*0x20; +5 kind byte,
        # grants u16 at +8..+0x16
        for i, b5 in case.get("lic_b5", {}).items():
            gm.w(IMG32 + 0x4000 + i * 0x20 + 5, bytes([b5 & 0xFF]))
        for i, grants in case.get("lic_grants", {}).items():
            for k, gr in enumerate(grants):
                gm.w(IMG32 + 0x4000 + i * 0x20 + 8 + k * 2,
                     struct.pack("<H", gr & 0xFFFF))

        # extra table bytes inside IMG32
        for off, b in case.get("img_bytes", []):
            gm.w(IMG32 + off, bytes(b))
        for off, v in case.get("img_words", []):
            gm.w(IMG32 + off, struct.pack("<H", v & 0xFFFF))
        for off, v in case.get("img_dwords", []):
            gm.w(IMG32 + off, dw(v))

        # unit + spawn
        gm.w(UNIT + 0x6A0, qw(SPAWN if case.get("has_spawn") else 0))
        gm.w(UNIT + 0xE80, bytes(case.get("unit_mask", [0] * 16)))
        gm.w(UNIT + 0xE90, dw(case.get("e90", 0)))
        gm.w(SPAWN + 0, bytes([case.get("spawn_flag", 0) & 0xFF]))
        gm.w(SPAWN + 0x78, bytes(case.get("spawn78", [0] * 5)))
        self.owns = case.get("owns", 1)

        self.trace, self.faults, self.fired = [], [], set()
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in HOOKS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        for s in STUBS:                      # real entry byte -> ret stub
            gm.w(s, b"\xc3")

    # -- hooks --

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        t = HOOKS[addr]
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        r9 = uc.reg_read(UC_X86_REG_R9)
        sp = uc.reg_read(UC_X86_REG_RSP)
        gm = self.gm
        if addr == FIND:
            self.trace.append("F")
            self._ret(UNIT if self.owns else 0)
        elif addr == VALID:
            self.trace.append("V%d:%X" % (rcx & 0xFFFFFFFF,
                                          rdx & 0xFFFF))
            self._watch_ret()
        elif addr == EQGATE:
            self.trace.append("E%02X" % gm.r(rcx + 9, 1)[0])
            self._watch_ret()
        elif addr == LICGATE:
            self.trace.append("L%02X" % (rcx & 0xFF))
            self._watch_ret()
        elif addr == APPLY:
            # callee rsp = caller rsp - 8: stack arg5 sits at +0x28
            mode = struct.unpack("<I", gm.r(sp + 0x28, 4))[0]
            self.trace.append("A%d+%d" % (rdx & 0xFFFFFFFF, mode))
            self._ret(0)
        elif addr == CASCADE:
            s5 = struct.unpack("<I", gm.r(sp + 0x28, 4))[0]
            s6 = struct.unpack("<I", gm.r(sp + 0x30, 4))[0]
            s7 = struct.unpack("<I", gm.r(sp + 0x38, 4))[0]
            self.trace.append("C%d:%d:%x:%d" % (r8 & 0xFFFFFFFF, s5,
                                                s6, s7))
            self._ret(0)
        elif addr == NOTIFY:
            self.trace.append("N")
            self._ret(0)
        elif addr == TAIL:
            self.trace.append("T%x" % (rdx & 0xFFFFFFFF))
            self._ret(0)
        elif t in ("e", "l", "R", "k"):
            pass                            # coverage only
        else:
            pass

    def _watch_ret(self):
        # one-shot: append "=retval" to the entry token when the call
        # returns. The hook stays installed but fires only once.
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", gm_r(self, sp, 8))[0]
        holder = {"fired": False}

        def on_ret(uc_, a, s, _u):
            if holder["fired"]:
                return
            holder["fired"] = True
            self.trace[-1] += "=%d" % s32x(uc_.reg_read(UC_X86_REG_RAX))

        uc.hook_add(UC_HOOK_CODE, on_ret, begin=back, end=back)

    def _ret(self, value):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", gm_r(self, sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RAX, value & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RIP, back)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


def gm_r(w, addr, n):
    return w.gm.r(addr, n)


def s32x(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, REC if not case.get("null_rec") else 0)
    uc.reg_write(UC_X86_REG_RDX, case.get("flags", 0))
    try:
        uc.emu_start(SUBJ, RETQ, count=2_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    gm = w.gm
    obs = {
        "ret": s32x(uc.reg_read(UC_X86_REG_RAX)),
        "hp": s32x(struct.unpack("<I", gm.r(REC + 0x48, 4))[0]),
        "mp": struct.unpack("<h", gm.r(REC + 0x4C, 2))[0],
        "w6": struct.unpack("<h", gm.r(REC + 6, 2))[0],
        "cpy": gm.r(REC + 0x40, 5).hex(),
        "spw": gm.r(SPAWN + 0x78, 5).hex(),
        "der": gm.r(REC + 0x78, 16).hex(),
    }
    return " ".join(w.trace) or "-", w.faults, w, obs


# ---- model --------------------------------------------------------------------

def model(case, g):
    """Expected trace + record effects from the documented semantics."""
    if case.get("null_rec"):
        # rcx=0: straight to the equipment loop with rbx=0; all reads
        # hit the mapped zero page. ids are 0 -> V=0 -> no E. owned bits
        # zero -> no L. acc empty vs prior 0 -> no A. N and T still run.
        tr = ["V6:0=0"] * 5 + ["N", "T%x" % (case.get("flags", 0) | 0x202)]
        return " ".join(tr), {"hp": 0, "mp": 0, "w6": 0,
                              "cpy": "0000000000", "spw": "0000000000",
                              "der": "00" * 16}
    acc = bytearray(16)
    tr = []
    kind = case.get("kind", 0)
    flags = case.get("flags", 0) | 0x202
    if kind == 0 and case.get("def_hdr") is not None:
        row = IMG32 + 0x1000 + case.get("row_idx", 0) * 0x40
        for i in range(32):
            if case.get("def_m0", 0) >> i & 1:
                acc[i // 8] |= 1 << (i % 8)
            if case.get("def_m1", 0) >> i & 1:
                acc[4 + i // 8] |= 1 << (i % 8)
    if kind == 1 and case.get("owns", 1):
        tr.append("F")
        um = case.get("unit_mask", [0] * 16)
        for i in range(128):
            if um[i // 8] >> (i % 8) & 1:
                acc[i // 8] |= 1 << (i % 8)
    elif kind == 1:
        tr.append("F")
    # equipment slots: the native loop always walks all five
    eq_ids5 = (list(case.get("equip_ids", [])) + [0] * 5)[:5]
    eq_ok = case.get("equip_hdr") is not None
    for k, ident in enumerate(eq_ids5):
        ok = 0
        if eq_ok:
            ok = g.valid6(ident, case.get("equip_count", 0), True)
        tr.append("V6:%X=%d" % (ident, ok))
        if not ok:
            continue
        row = IMG32 + 0x2000 + (ident - 0x1000) * 0x20
        b9 = case.get("eq_t9", {}).get(ident, 0)
        gv = g.eq_gate(b9)
        tr.append("E%02X=%d" % (b9, gv))
        if gv == 3:
            st = case.get("eq_st", {}).get(ident, 0xFF)
            if st != 0xFF and st < 128:
                acc[st // 8] |= 1 << (st % 8)
    # licence walk: ids 0..360, owned bit first
    lic_ok = case.get("lic_hdr") is not None
    for i in sorted(case.get("lic_owned", [])):
        if i > 360:
            continue                       # the walk stops at 360
        # the gate's argument is the ROW's +5 byte: 0 when the table or
        # the resolve is absent, not the planted value
        b5 = case.get("lic_b5", {}).get(i, 0) if lic_ok else 0
        gv = g.lic_gate(b5)
        tr.append("L%02X=%d" % (b5, gv))
        if gv == 2:
            for gr in case.get("lic_grants", {}).get(i, []):
                if gr != 0xFFFF and gr < 128:
                    acc[gr // 8] |= 1 << (gr % 8)
    # diff vs prior: rec+0x7C (g7c) sits inside the prior block, so the
    # planted byte overwrites prior[4] in the guest image
    prior = bytearray(case.get("prior", [0] * 16))
    prior[4] = case.get("g7c", 0) & 0xFF
    for i in range(128):
        a = acc[i // 8] >> (i % 8) & 1
        p = prior[i // 8] >> (i % 8) & 1
        if a and not p:
            tr.append("A%d+3" % i)
        elif p and not a:
            tr.append("A%d+1" % i)
    tr.append("N")
    # kind1 tail
    if kind == 1:
        tr.append("F")
        if case.get("owns", 1):
            for b in range(32):
                if case.get("e90", 0) >> b & 1:
                    tr.append("C%d:0:%x:5" % (b, flags))
    if kind == 1:
        tr.append("F")
    tr.append("T%x" % flags)
    # record effects
    cpy = bytes(case.get("rec40", [0] * 5))
    spw = bytes(case.get("spawn78", [0] * 5))
    if kind == 1 and case.get("owns", 1) and case.get("has_spawn"):
        if case.get("spawn_flag", 0) & 0x80:
            cpy = spw
        else:
            spw = cpy
    pres = case.get("pres64", 0) | case.get("pres3c", 0)
    hp = case.get("hp", 0)
    if not pres & 0x10000:
        cap = case.get("maxhp", 0)
        if pres & 0x10000000:
            cap = cap * 2 & 0xFFFFFFFF
            cap = cap - 0x100000000 if cap & 0x80000000 else cap
        if hp > cap:
            hp = cap
    denied = (case.get("g6c", 0) & 0x80) or (case.get("g7c", 0) & 0x80)
    stat = case.get("stat28", 0)
    mp = case.get("mp", 0)
    cap2 = 0 if denied else stat
    if mp > cap2:
        mp = cap2
    w6 = case.get("w6", 0)
    cap3 = 0 if denied else stat * (case.get("mult37", 0) or 1)
    if w6 > cap3:
        w6 = cap3
    return " ".join(tr) or "-", {
        "hp": hp, "mp": mp, "w6": w6,
        "cpy": cpy.hex(), "spw": spw.hex(),
        "der": prior.hex()}


# ---- cases --------------------------------------------------------------------

W = dict(def_hdr=0x100, equip_hdr=0x200, lic_hdr=0x300)


def build_cases():
    C = []

    def A(name, **kw):
        kw.setdefault("owns", 1)
        kw.setdefault("has_spawn", True)
        C.append(dict(W, **kw, name=name))

    # kind-0 definition-row masks -> acc bits 0..63
    A("def-masks", kind=0, row_idx=0, def_m0=0x5, def_m1=0x3)
    A("def-masks-hi", kind=0, row_idx=0, def_m0=0x80000001,
      def_m1=0x80000001)
    # failed resolve: no def slot -> masks read from page 0 (zeros)
    A("def-slot-null", kind=0, def_hdr=None, row_idx=0)
    # row index selects the row (idx 2 -> 0x1000+0x80)
    A("def-row2", kind=0, row_idx=2, def_m0=0x7)

    # equipment: arm-6 validity over equip_count
    eq_ids = [0x1000, 0x1001, 0x1002, 0x1003, 0x1004]
    A("eq-all-contrib", kind=0, equip_ids=eq_ids, equip_count=5,
      eq_t9={i: 0x13 for i in eq_ids},
      eq_st={0x1000: 0x20, 0x1001: 0x21, 0x1002: 0x22,
             0x1003: 0x23, 0x1004: 0x24})
    A("eq-invalid-id", kind=0, equip_ids=eq_ids, equip_count=2,
      eq_t9={i: 0x13 for i in eq_ids},
      eq_st={i: 0x20 + k for k, i in enumerate(eq_ids)})
    A("eq-below-base", kind=0, equip_ids=[0x0FFF] + eq_ids[1:],
      equip_count=5, eq_t9={i: 0x13 for i in eq_ids},
      eq_st={i: 0x30 + k for k, i in enumerate(eq_ids)})
    A("eq-null-table", kind=0, equip_hdr=None, equip_ids=eq_ids,
      equip_count=5, eq_t9={i: 0x13 for i in eq_ids})
    # kind gate: only types mapping to class 7..9 (gate 3) contribute
    A("eq-gate2-type", kind=0, equip_ids=[0x1000], equip_count=5,
      eq_t9={0x1000: 0x12}, eq_st={0x1000: 0x40})     # class 6 -> 2
    A("eq-gate1-type", kind=0, equip_ids=[0x1000], equip_count=5,
      eq_t9={0x1000: 0x00}, eq_st={0x1000: 0x40})     # class 1 -> 1
    A("eq-gate0-type", kind=0, equip_ids=[0x1000], equip_count=5,
      eq_t9={0x1000: 0x1B}, eq_st={0x1000: 0x40})     # >0x1A -> 0
    A("eq-cls5-type", kind=0, equip_ids=[0x1000], equip_count=5,
      eq_t9={0x1000: 0x17}, eq_st={0x1000: 0x50})     # class 5 -> 1
    A("eq-gate3-alt", kind=0, equip_ids=[0x1000], equip_count=5,
      eq_t9={0x1000: 0x16}, eq_st={0x1000: 0x41})     # class 9 -> 3
    A("eq-ff-sentinel", kind=0, equip_ids=[0x1000], equip_count=5,
      eq_t9={0x1000: 0x14}, eq_st={0x1000: 0xFF})     # gate3 but no status

    # licence: row+5 byte -> class -> gate; gate==2 grants
    A("lic-grant", kind=0, lic_owned=[0],
      lic_b5={0: 0x0F}, lic_grants={0: [0x10, 0x11, 0xFFFF, 0xFFFF,
                                       0xFFFF, 0xFFFF, 0xFFFF, 0x12]})
    A("lic-gate1", kind=0, lic_owned=[0],
      lic_b5={0: 0x09}, lic_grants={0: [0x10] + [0xFFFF] * 7})
    A("lic-gate0", kind=0, lic_owned=[0],
      lic_b5={0: 0x01}, lic_grants={0: [0x10] + [0xFFFF] * 7})
    A("lic-gate3", kind=0, lic_owned=[0],
      lic_b5={0: 0x1E}, lic_grants={0: [0x10] + [0xFFFF] * 7})
    A("lic-gate-neg", kind=0, lic_owned=[0],
      lic_b5={0: 0x16}, lic_grants={0: [0x10] + [0xFFFF] * 7})
    A("lic-null-table", kind=0, lic_hdr=None, lic_owned=[0],
      lic_b5={0: 0x0F}, lic_grants={0: [0x10] + [0xFFFF] * 7})
    A("lic-id-360", kind=0, lic_owned=[360],
      lic_b5={360: 0x0F}, lic_grants={360: [0x44] + [0xFFFF] * 7})
    A("lic-id-361-unseen", kind=0, lic_owned=[361],
      lic_b5={361: 0x0F}, lic_grants={361: [0x44] + [0xFFFF] * 7})
    A("lic-multi", kind=0, lic_owned=[0, 3, 15],
      lic_b5={0: 0x0F, 3: 0x0F, 15: 0x0F},
      lic_grants={0: [0x50] + [0xFFFF] * 7, 3: [0x51] + [0xFFFF] * 7,
                  15: [0x52] + [0xFFFF] * 7})

    # diff: prior set -> removals and adds interleaved
    pr = [0] * 16
    pr[0] = 0x0F
    A("diff-add-rem", kind=0, prior=pr, def_m0=0x3)  # 0,1 stay; 2,3 out
    pr2 = [0] * 16
    pr2[0] = 0xFF
    A("diff-all-rem", kind=0, prior=pr2)

    # kind 1: unit mask, cascade, spawn exchange
    um = [0] * 16
    um[0] = 0xF; um[8] = 1
    A("k1-mask-cascade", kind=1, unit_mask=um, e90=0x5)
    A("k1-no-unit", kind=1, owns=0, unit_mask=um, e90=0xFF)
    A("k1-spawn-in", kind=1, unit_mask=[0] * 16, e90=0,
      spawn_flag=0x80, spawn78=[0x11, 0x22, 0x33, 0x44, 0x55],
      rec40=[0xA1, 0xA2, 0xA3, 0xA4, 0xA5])
    A("k1-spawn-out", kind=1, unit_mask=[0] * 16, e90=0,
      spawn_flag=0x01, spawn78=[0x11, 0x22, 0x33, 0x44, 0x55],
      rec40=[0xA1, 0xA2, 0xA3, 0xA4, 0xA5])
    A("k1-no-spawn", kind=1, unit_mask=um, e90=0, has_spawn=False)

    # clamps (regression)
    A("clamp-hp", kind=0, hp=100, maxhp=50)
    A("clamp-hp-double", kind=0, hp=100, maxhp=50, pres64=0x10000000)
    A("clamp-hp-freeze", kind=0, hp=100, maxhp=50, pres64=0x10000)
    A("clamp-mp", kind=0, mp=100, stat28=0x20)
    A("clamp-mp-deny6c", kind=0, mp=100, stat28=0x20, g6c=0x80)
    A("clamp-mp-deny7c", kind=0, mp=100, stat28=0x20, g7c=0xFF)
    A("clamp-w6", kind=0, w6=100, stat28=0x10, mult37=3)
    A("clamp-w6-mult0", kind=0, w6=100, stat28=0x10, mult37=0)

    # flag word reaches APPLY/CASCADE args
    A("flags-flow", kind=1, unit_mask=um, e90=1, flags=0xFFFF)

    # null record
    A("null-rec", null_rec=True)
    return C


# ---- mutants -------------------------------------------------------------------

MUTANTS = [
    ("m-val-base", 0x322D0A, b"\x01",
     "arm6 base 0x1000 -> 0x1001: id 0x1000 fails validity"),
    ("m-val-hi",   0x322D16, b"\xff\x0f",
     "arm6 lea +0x1000 -> +0x0FFF: last valid id excluded"),
    ("m-val-jl",   0x323030, b"\x8d",
     "tail jl -> jge: every id fails the lower bound"),
    ("m-val-jg",   0x32303B, b"\x8e",
     "tail jg -> jle: every id fails the upper bound"),
    ("m-eq-bnd",   0x31E9F6, b"\x10",
     "eq class bound 0x1A -> 0x10: types >=0x11 -> class 0"),
    ("m-eq-cmp5",  0x31E9AF, b"\x04",
     "remap cmp 5 -> 4: class 5 falls through to 0"),
    ("m-eq-sub7",  0x31E9B9, b"\xf8",
     "remap add -7 -> -8: class 7 -> gate 0, type 0x13 stops"),
    ("m-lic-bnd",  0x3241D4, b"\x0e",
     "lic class bound 0x1D -> 0x0E: bytes >0x0F -> class 0"),
    ("m-lic-dec",  0x3241D0, b"\xc1",
     "lic dec ecx -> inc ecx: class lookup shifts one"),
    ("m-lic-add",  0x32389B, b"\xec",
     "gate map add -0x15 -> -0x14: class window shifts"),
    ("m-lic-cmp2", 0x31019D, b"\x01",
     "subject lic cmp 2 -> 1: gate-1 rows contribute"),
    ("m-eq-cmp3",  0x3100EC, b"\x02",
     "subject eq cmp 3 -> 2: gate-2 rows contribute"),
    ("m-kind1",    0x31001F, b"\x74",
     "kind!=1 skip -> je: kind-0 runs the unit-mask loop"),
]


def main():
    raw, secs = load_image()
    g = GateModel(raw, secs)
    out = {"exe_sha256": SHA, "cases": [], "mutants": []}
    npass = nfail = 0
    results = {}
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs)
        exp_tr, exp_obs = model(case, g)
        ok = (tr == exp_tr and not [f for f in faults if f[0] == "MEM"]
              and all(obs[k] == v for k, v in exp_obs.items()))
        npass += ok
        nfail += (not ok)
        results[case["name"]] = (tr, obs)
        if not ok:
            print("FAIL %s\n  got:  %s\n  want: %s\n  obs %s vs %s\n  faults=%s"
                  % (case["name"], tr, exp_tr, obs, exp_obs, faults))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "trace": tr, "ok": bool(ok),
                             "obs": obs, "exp_trace": exp_tr,
                             "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))

    fired = set()
    for case in build_cases():
        tr, faults, w, obs = run_case(case, raw, secs)
        fired |= w.fired
    out["bodies_fired"] = ["0x%X" % v for v in sorted(fired)]
    print("fired:", " ".join("%s@%x" % (HOOKS[v], v) for v in sorted(fired)))

    base = {c["name"]: results[c["name"]] for c in build_cases()}
    for name, va, data, why in MUTANTS:
        n_diff, diffs = 0, []
        for case in build_cases():
            c = dict(case)
            c["patch_bytes"] = [(va, data)]
            tr, faults, w, obs = run_case(c, raw, secs)
            if (tr, obs) != base[case["name"]] or \
               [f for f in faults if f[0] == "MEM"]:
                n_diff += 1
                diffs.append((case["name"], "tr=%s" % tr))
        killed = n_diff > 0
        print(("KILL " if killed else "SURV") + " %s  (%d divergent) %s"
              % (name, n_diff, why))
        out["mutants"].append({"name": name, "va": "0x%X" % va,
                               "killed": killed, "divergent": n_diff,
                               "why": why, "sample": diffs[:3]})
    json.dump(out, open("result.json", "w"), indent=1,
              default=lambda o: o.hex() if isinstance(o, bytes) else str(o))
    return 0 if nfail == 0 and all(m["killed"] for m in out["mutants"]) else 1


if __name__ == "__main__":
    sys.exit(main())
