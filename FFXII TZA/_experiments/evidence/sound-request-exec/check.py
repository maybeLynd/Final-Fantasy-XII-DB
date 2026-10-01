#!/usr/bin/env python3
"""EXP-096 sound-request-exec - the sound-request path executed as real
shipped bodies from the script verb down to the dispatcher boundary.

Subject under test (per CONTRACT-sound-request.md): the chain
    00357040 (sebsoundplay_2c1 verb) / 00249C60 family wrappers
        -> resolver 003A1180 / 003A11F0 / 003A1070 / 003A1100
        -> play call 002DF220 (masking) -> dispatcher 001DBDB0

The contract's mutation campaign proved the *model*; its §12 lists six
scripted leaf callees. This experiment executes five of them real:
liveness 00267330, both resolver gates 003A1180/003A11F0 (plus selector
targets 003A1070/003A1100), VM pop 00267E10 and push 0026B4E0, and the
play call 002DF220 whose masking (pan->sil 8 bits, volume->&0x7F,
handle btr 31) produces the dispatch arguments the contract compares.

    001DBDB0  dispatcher - SCRIPTED at entry: logs (rcx,rdx,r8,r9) and
              returns a scripted value. Its 174-body closure (Seb/Sep fork
              00210C00 + controllers/bank managers) is a disclosed boundary;
              the observable that matters - the four dispatch args - is
              captured at its entry point.
    001DBE90  dispatcher-B (0024A1A0 path) - SCRIPTED at entry, args logged.
    002DEE80  readiness test - SCRIPTED: its ecx!=0 arm tail-jumps into the
              dispatcher-B machinery (001DBCE0), same disclosed boundary.
    008620C0  vmpop type>2 error path - SCRIPTED ret 0.

Real and verified end-to-end:
    - gate1 0x2091098 (dword) on 00249C60/00249CA0/0024A1A0; 00271500 omits it
    - liveness 00267330: byte[slot*0x288 + 0x2098E20 + 0x10] - bit0 clear ->
      refuse(1); else returns bit7
    - handle dwords 0x2AEF3FC / 0x2AEF400 / 0x2AEF404; -1 -> refuse
    - handle table 0x2AEEDC0, 64 x 24B: slot = handle low16, entry {+8 lo,
      +0xA hi}; (hi<<16|lo) must equal handle&0x7FFFFFFF; ret lo<<9 + arg
    - play 002DF220: id==-1 -> ret 0; gate2 byte 0x22CB726 (via 003603C0)
      nonzero -> ret 0; else dispatch(0, id&~bit31, pan&0xFF, vol&0x7F)
    - verb 00357040: 4 typed pops (arg4,3,2,1 = volume,pan,index,selector),
      selector 1->003A1100 / 2->003A1070 / else->003A1180, mute predicate
      00267310 on cmdrec+0x15's slot byte +0, push via 0026B4E0
    - 0024A1A0: gate1 -> refuse; readiness 002DEE80 -> reshape 002DF0F0
      (real) -> 001DBE90 (stub)

NOT EXERCISED (disclosed): everything past the dispatcher entries - the
Seb/Sep fork, controllers, bank managers, voice. The 00210C00 fork stays
unexecuted exactly as the contract's pilot left it.
"""
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
CODE   = 0x63000000

VMSTK  = HEAP + 0x100000        # vm stack ctx (vmpop/vmpush operand)
CMDREC = HEAP + 0x110000        # command record (+0x15 mute slot idx)
OCTX   = HEAP + 0x120000        # outer ctx (vmpush: +0x11 slot, +0xA8 buf)
RESBUF = HEAP + 0x130000        # vmpush result buffer (40B slots)

VERB   = 0x00357040
W_C60  = 0x00249C60
W_CA0  = 0x00249CA0
W_1500 = 0x00271500
W_A1A0 = 0x0024A1A0
RES_A  = 0x003A1180            # gate-A resolver (liveness + handle A)
RES_B  = 0x003A11F0            # gateless resolver (handle A, no liveness)
RES_70 = 0x003A1070            # gate + liveness + handle B
RES_100 = 0x003A1100           # gate + liveness + handle at 0x2AEF400
LIVE   = 0x00267330            # liveness predicate
MUTE   = 0x00267310            # per-slot byte read (mute predicate)
PLAY   = 0x002DF220            # masking play call
GATE2  = 0x003603C0            # second gate reader
DISP   = 0x001DBDB0            # dispatcher (STUB)
DISPB  = 0x001DBE90            # dispatcher-B (STUB)
RESHAPE = 0x002DF0F0           # 0024A1A0's reshape tail (real)
READY  = 0x002DEE80            # readiness test (STUB: deep arm)
VPOP   = 0x00267E10
VPUSH  = 0x0026B4E0
VERR   = 0x008620C0            # vmpop type>2 error (STUB)

G1     = 0x02091098            # wrapper gate1 dword
G2B    = 0x022CB726            # gate2 byte read by 003603C0
SLOTS  = 0x02098E20            # ActorManager slot array, stride 0x288
HDLA   = 0x02AEF3FC            # handle A dword
HDLGB  = 0x02AEF400            # shared gate dword (and 003A1100's handle)
HDLB   = 0x02AEF404            # handle B dword
TBL    = 0x02AEEDC0            # handle table, 64 x 24B; +8 lo16, +0xA hi16

COOKIE   = 0x0000DEADBEEF
G_COOKIE = 0x1F44830

CALLS = {
    VERB:   "verb",
    W_C60:  "w_c60",  W_CA0: "w_ca0",  W_1500: "w_1500", W_A1A0: "w_a1a0",
    RES_A:  "resA",   RES_B: "resB",   RES_70: "res70",  RES_100: "res100",
    LIVE:   "live",   MUTE:  "mute",
    PLAY:   "play",   GATE2: "gate2",
    DISP:   "disp",   DISPB: "dispB",
    RESHAPE: "resh",  READY: "ready",
    VPOP:   "vpop",   VPUSH: "vpush",
    VERR:   "verr",
    0x00808C40: "cookie",
}
STUBS = {DISP: "disp", DISPB: "dispB", READY: "ready", VERR: "verr"}

def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def db(v): return struct.pack("<B", v & 0xFF)

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
    iat = []
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
        j = 0
        while True:
            e = struct.unpack_from("<Q", raw, rva2off(ilt or iat_rva) + 8 * j)[0]
            if e == 0:
                break
            iat.append(BASE + iat_rva + 8 * j)
            j += 1
        i += 1
    return raw, secs, iat

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

def mk_handle(hi, slot, flag31=0):
    return ((hi << 16) | slot | (flag31 << 31)) & 0xFFFFFFFF

def plant_entry(gm, slot, lo, hi):
    gm.w(TBL + slot * 24 + 8, hw(lo))
    gm.w(TBL + slot * 24 + 0xA, hw(hi))

class World:
    def __init__(self, case, raw, secs, iat):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc)
        img = bytearray(IMG_HI - IMG_LO)
        for va, vs, ra, rs in secs:
            n = min(vs, rs)
            img[va:va + n] = raw[ra:ra + n]
        self.gm.map(IMG_LO, len(img), bytes(img))
        for a, s in [(HEAP, 0x400000), (STACK, 0x100000), (RETQ, 0x1000),
                     (CODE, 0x1000)]:
            self.gm.map(a, s)
        gm = self.gm
        gm.w(RETQ, b"\xc3")
        for va in STUBS:
            gm.w(va, b"\xc3")
        for slot in iat:
            gm.w(slot, qw(0))

        # ---- globals
        gm.w(G_COOKIE, qw(COOKIE))
        gm.w(G1, dw(case.get("g1", 0)))
        gm.w(G2B, db(case.get("g2", 0)))
        gm.w(HDLA, dw(case.get("hdlA", 0xFFFFFFFF)))
        gm.w(HDLGB, dw(case.get("hdlGB", 0xFFFFFFFF)))
        gm.w(HDLB, dw(case.get("hdlB", 0xFFFFFFFF)))
        for slot, lo, hi in case.get("tbl", []):
            plant_entry(gm, slot, lo, hi)
        # ActorManager slots: 00267330 reads slot*0x288+0x2098E10+0x10
        # (= +0 rel SLOTS); 00267310 reads slot*0x288+0x2099011 (= +0x1F1).
        for slot, b in case.get("slots_live", []):
            gm.w(SLOTS + slot * 0x288, db(b))
        for slot, b in case.get("slots_mute", []):
            gm.w(SLOTS + slot * 0x288 + 0x1F1, db(b))

        # ---- vm stack ctx: count dword, type bytes at +4+i, values
        #      dword at +0x184+i*4.  Stack order = push order; the verb pops
        #      top-first: arg4(pan), arg3(vol), arg2(idx), arg1(sel).
        vs = case.get("vstack", [])          # list of (type, value) top LAST
        gm.w(VMSTK, dw(len(vs)))
        for i, (ty, val) in enumerate(vs):
            gm.w(VMSTK + 4 + i, db(ty))
            gm.w(VMSTK + 0x184 + i * 4, dw(val))

        # ---- command record / outer ctx
        gm.w(CMDREC + 0x15, db(case.get("mute_slot", 0)))
        gm.w(OCTX + 0x11, db(case.get("push_slot", 0)))
        gm.w(OCTX + 0xA8, qw(RESBUF))

        self.disp_ret = case.get("disp_ret", 0x5A)
        self.dispb_ret = case.get("dispb_ret", 0x5B)
        self.ready_ret = case.get("ready_ret", 1)
        self.trace, self.faults = [], []
        self.fired = set()

        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)

        self.calls = []
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in CALLS:
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def _ret(self, value):
        sp = self.uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.uc.mem_read(sp, 8))[0]
        self.uc.reg_write(UC_X86_REG_RSP, sp + 8)
        self.uc.reg_write(UC_X86_REG_RAX, value & 0xFFFFFFFFFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_RIP, back)

    def on_call(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8  = uc.reg_read(UC_X86_REG_R8)  & 0xFFFFFFFFFFFFFFFF
        r9  = uc.reg_read(UC_X86_REG_R9)  & 0xFFFFFFFFFFFFFFFF
        self.fired.add(addr)
        name = CALLS[addr]
        if addr == VPOP:
            # ecx-free: arg is rcx=ctx. Log popped value AFTER ret is awkward;
            # instead log the pre-pop count so order is observable.
            cnt = struct.unpack("<I", self.gm.r(rcx, 4))[0]
            self.trace.append(("o%d" % cnt,))
            return
        if addr == VPUSH:
            self.trace.append(("W%x" % (rdx & 0xFFFFFFFF),))
            return
        if addr == DISP:
            self.trace.append(("D%x" % rcx, "h%x" % rdx,
                               "p%x" % (r8 & 0xFFFFFFFF), "v%x" % (r9 & 0xFFFFFFFF)))
            self._ret(self.disp_ret)
            return
        if addr == DISPB:
            self.trace.append(("DB%x" % rcx, "h%x" % rdx,
                               "a%x" % r8, "b%x" % r9))
            self._ret(self.dispb_ret)
            return
        if addr == READY:
            self.trace.append(("Rd%x" % (rcx & 0xFFFFFFFF),))
            self._ret(self.ready_ret)
            return
        if addr == VERR:
            self.trace.append(("Ve%d" % (rcx & 0xFFFFFFFF),))
            self._ret(0)
            return
        if addr in (RES_A, RES_B, RES_70, RES_100):
            self.trace.append(("%s%x" % (name, rcx & 0xFFFFFFFF),))
            return
        if addr in (LIVE, MUTE):
            self.trace.append(("%s%x" % (name[:1], rcx & 0xFFFFFFFF),))
            return
        if addr == PLAY:
            self.trace.append(("Y%x" % (rcx & 0xFFFFFFFF), "%x" % (rdx & 0xFFFFFFFF),
                               "%x" % (r8 & 0xFFFFFFFF)))
            return
        if addr in (VERB, GATE2):
            self.trace.append((name,))
            return
        if addr in (W_C60, W_CA0, W_1500, W_A1A0, RESHAPE):
            self.trace.append(("%s%x" % (name, rcx & 0xFFFFFFFF),))
            return
        self.calls.append((name, "rcx=%x" % rcx, "rdx=%x" % rdx,
                           "r8=%x" % r8, "r9=%x" % r9))

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False

def run_case(case, raw, secs, iat):
    w = World(case, raw, secs, iat)
    uc, gm = w.uc, w.gm
    entry = case["entry"]
    sp = STACK + 0x80000
    gm.w(sp, qw(RETQ))
    gm.w(sp + 0x28, b"\xCD" * 0x30)
    uc.reg_write(UC_X86_REG_RSP, sp)
    uc.reg_write(UC_X86_REG_RCX, case.get("rcx", 0) & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_RDX, case.get("rdx", 0) & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_R8,  case.get("r8",  0) & 0xFFFFFFFFFFFFFFFF)
    uc.reg_write(UC_X86_REG_R9,  case.get("r9",  0) & 0xFFFFFFFFFFFFFFFF)
    try:
        uc.emu_start(entry, RETQ, count=4_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))
    ret = ctypes.c_int32(uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF).value
    tr = " ".join(" ".join(t) for t in w.trace)
    # vmpush effect check: slot k at RESBUF+k*40: +0x15=2, +0xC=value
    k = case.get("push_slot", 0)
    pushed_type = gm.r(RESBUF + k * 40 + 0x15, 1)[0]
    pushed_val = struct.unpack("<i", gm.r(RESBUF + k * 40 + 0xC, 4))[0]
    extra = {"push_type": pushed_type, "push_val": pushed_val}
    return ret, (tr if tr else "-"), w.faults, w, extra

# ---- cases -------------------------------------------------------------------

def vstack(sel, idx, pan, vol, ty=1):
    """push order bottom->top: sel(arg1) idx(arg2) pan(arg3) vol(arg4)."""
    return [(ty, sel), (ty, idx), (ty, pan), (ty, vol)]

GOOD_A = dict(hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)], slots_live=[(0, 0x01)])
GOOD_B = dict(hdlGB=mk_handle(9, 4), tbl=[(4, 4, 9)], slots_live=[(0, 0x01)])
GOOD_C = dict(hdlGB=0, hdlB=mk_handle(5, 2), tbl=[(2, 2, 5)],
              slots_live=[(0, 0x01)])

def build_cases():
    C_ = []
    def A(name, ret, trace, **kw):
        C_.append(dict(kw, name=name, want_ret=ret, want_trace=trace))

    # --- verb end-to-end: sel0/9 -> resA(=slot3 -> id 0x600+idx)
    A("verb-sel0", None, "verb o4 o3 o2 o1 resA5 l0 m0 Y605 40 7f gate2 D0 h605 p40 v7f W5a",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(0, 5, 0x40, 0x7F), **GOOD_A)
    A("verb-sel9", None, "verb o4 o3 o2 o1 resA5 l0 m0 Y605 40 7f gate2 D0 h605 p40 v7f W5a",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(9, 5, 0x40, 0x7F), **GOOD_A)
    # sel1 -> res100 uses HDLGB as BOTH gate and handle (slot4 -> id 0x800+idx)
    A("verb-sel1", None, "verb o4 o3 o2 o1 res1006 l0 m0 Y806 40 7f gate2 D0 h806 p40 v7f W5a",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(1, 6, 0x40, 0x7F), **GOOD_B)
    # sel2 -> res70: gate HDLGB!=-1, handle HDLB (slot2 -> id 0x400+idx)
    A("verb-sel2", None, "verb o4 o3 o2 o1 res705 l0 m0 Y405 40 7f gate2 D0 h405 p40 v7f W5a",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(2, 5, 0x40, 0x7F), **GOOD_C)
    # masking: pan 0x2FF -> p ff, vol 0x1FF -> v 7f
    A("verb-mask", None, "verb o4 o3 o2 o1 resA5 l0 m0 Y605 2ff 1ff gate2 D0 h605 pff v7f W5a",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(0, 5, 0x2FF, 0x1FF), **GOOD_A)
    # mute: slot0 byte+0 nonzero -> play skipped, push 0
    A("verb-muted", None, "verb o4 o3 o2 o1 resA5 l0 m0 W0",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(0, 5, 0x40, 0x7F), slots_mute=[(0, 1)], **GOOD_A)
    # resolver refuses (handle -1): play sees id -1 -> ret 0, no dispatch
    A("verb-resfail", None, "verb o4 o3 o2 o1 resA5 l0 m0 Yffffffff 40 7f W0",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(0, 5, 0x40, 0x7F), slots_live=[(0, 0x01)])
    # gate2 set: play returns 0 before dispatch
    A("verb-gate2", None, "verb o4 o3 o2 o1 resA5 l0 m0 Y605 40 7f gate2 W0",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK, g2=1,
      vstack=vstack(0, 5, 0x40, 0x7F), **GOOD_A)
    # liveness refuses: slot0 byte 0 -> resA -1 -> play id -1 -> W0
    A("verb-held", None, "verb o4 o3 o2 o1 resA5 l0 m0 Yffffffff 40 7f W0",
      entry=VERB, rcx=OCTX, rdx=CMDREC, r9=VMSTK,
      vstack=vstack(0, 5, 0x40, 0x7F),
      hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)], slots_live=[(0, 0x00)])

    # --- wrappers direct (rcx = local index)
    A("w-c60-ok", 0x5A, "w_c605 resA5 l0 Y605 40 7f gate2 D0 h605 p40 v7f",
      entry=W_C60, rcx=5, **GOOD_A)
    A("w-c60-gate1", -1, "w_c605",
      entry=W_C60, rcx=5, g1=1, **GOOD_A)
    A("w-1500-gate1", 0x5A, "w_15005 resA5 l0 Y605 40 7f gate2 D0 h605 p40 v7f",
      entry=W_1500, rcx=5, g1=1, **GOOD_A)   # no gate: proceeds anyway
    A("w-ca0-ok", 0x5A, "w_ca05 resB5 Y605 40 7f gate2 D0 h605 p40 v7f",
      entry=W_CA0, rcx=5, **GOOD_A)
    # resB has NO liveness call - dead world still resolves (contract §5)
    A("w-ca0-dead", 0x5A, "w_ca05 resB5 Y605 40 7f gate2 D0 h605 p40 v7f",
      entry=W_CA0, rcx=5, hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)],
      slots_live=[(0, 0x00)])
    A("w-ca0-gate1", -1, "w_ca05",
      entry=W_CA0, rcx=5, g1=1, **GOOD_A)
    # resolver refuses -> wrapper ret -1 (its own or eax,-1, not play's 0)
    A("w-c60-resfail", -1, "w_c605 resA5 l0",
      entry=W_C60, rcx=5, slots_live=[(0, 0x01)])
    # 0024A1A0: gate1 -> refuse(0! not -1); else ready->reshape->dispB
    A("w-a1a0-gate1", None, "w_a1a05", entry=W_A1A0, rcx=5, g1=1)
    A("w-a1a0-ok", None, "w_a1a05 Rd5 resh5 DB1 h5 a0 b0",
      entry=W_A1A0, rcx=5)     # reshape(edx=0!=-1): ecx=~(0)>>31=1, r8=0
    # --- resolvers direct
    A("resA-ok", 0x605, "resA5 l0", entry=RES_A, rcx=5, **GOOD_A)
    A("resA-dead", -1, "resA5 l0", entry=RES_A, rcx=5,
      hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)], slots_live=[(0, 0x00)])
    A("resA-bit7", -1, "resA5 l0", entry=RES_A, rcx=5,
      hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)], slots_live=[(0, 0x81)])
    A("resA-hdlm1", -1, "resA5 l0", entry=RES_A, rcx=5,
      slots_live=[(0, 0x01)])
    A("resA-mismatch", -1, "resA5 l0", entry=RES_A, rcx=5,
      hdlA=mk_handle(7, 3), tbl=[(3, 9, 9)], slots_live=[(0, 0x01)])
    A("resA-flag31", 0x605, "resA5 l0", entry=RES_A, rcx=5,
      hdlA=mk_handle(7, 3, flag31=1), tbl=[(3, 3, 7)], slots_live=[(0, 0x01)])
    A("resB-dead-ok", 0x605, "resB5", entry=RES_B, rcx=5,
      hdlA=mk_handle(7, 3), tbl=[(3, 3, 7)], slots_live=[(0, 0x00)])
    A("resB-hdlm1", -1, "resB5", entry=RES_B, rcx=5)
    A("res70-gatem1", -1, "res705", entry=RES_70, rcx=5,
      hdlB=mk_handle(5, 2), tbl=[(2, 2, 5)], slots_live=[(0, 0x01)])
    A("res70-ok", 0x405, "res705 l0", entry=RES_70, rcx=5, **GOOD_C)
    A("res100-gatem1", -1, "res1005", entry=RES_100, rcx=5,
      slots_live=[(0, 0x01)])
    A("res100-ok", 0x805, "res1005 l0", entry=RES_100, rcx=5, **GOOD_B)
    # --- play call direct
    A("play-idm1", 0, "Yffffffff 40 7f", entry=PLAY, rcx=-1, rdx=0x40, r8=0x7F)
    A("play-gate2", 0, "Y605 40 7f gate2", entry=PLAY, rcx=0x605,
      rdx=0x40, r8=0x7F, g2=1)
    A("play-ok", 0x5A, "Y605 40 7f gate2 D0 h605 p40 v7f",
      entry=PLAY, rcx=0x605, rdx=0x40, r8=0x7F)
    A("play-mask", 0x5A, "Y80000605 3ff 1ff gate2 D0 h605 pff v7f",
      entry=PLAY, rcx=0x80000605, rdx=0x3FF, r8=0x1FF)
    # --- vmpop shapes
    A("vpop-int", 0x11223344, "o1", entry=VPOP, rcx=VMSTK,
      vstack=[(1, 0x11223344)])
    A("vpop-float", 3, "o1", entry=VPOP, rcx=VMSTK,
      vstack=[(2, 0x40400000)])          # 3.0f -> cvttss2si 3
    A("vpop-empty", 0, "o0", entry=VPOP, rcx=VMSTK, vstack=[])
    A("vpop-type3", 0, "o1 Ve1", entry=VPOP, rcx=VMSTK, vstack=[(3, 0x55)])
    # --- vmpush write shape (result slot k: +0x15=2, +0xC=val)
    A("vpush-wr", None, "W11223344", entry=VPUSH, rcx=OCTX, rdx=0x11223344,
      push_slot=1, want_push=(2, 0x11223344))
    return C_

# ---- mutants -----------------------------------------------------------------
# (name, va, bytes, why-killed). Sites verified against shipped bytes.

MUTANTS = [
    ("m-volmask",  0x2DF258, db(0xFF),
     "and edi,0x7F -> 0xFF: volume keeps bit7"),
    ("m-pantrunc", 0x2DF259, bytes.fromhex("440FB7C6"),
     "movzx r8d,sil -> si: pan keeps high byte"),
    ("m-btr",      0x2DF25D, b"\x90" * 4,
     "btr ebx,0x1f removed: dispatch sees flagged handle"),
    ("m-playm1",   0x2DF238, db(0x00),
     "cmp ecx,-1 -> cmp ecx,0: id 0 refused, -1 dispatched"),
    ("m-gate2",    0x3603C0, bytes.fromhex("31C09090909090"),
     "gate2 always 0: transition gate disabled"),
    ("m-wgate",    0x249C6B, db(0x74),
     "00249C60 gate1 jne->je: gate set now proceeds"),
    ("m-wret",     0x249C8B, bytes.fromhex("31C090"),
     "or eax,-1 -> xor eax: refusal returns 0"),
    ("m-resbtr",   0x3A11AF, b"\x90" * 5,
     "btr r8d,0x1f removed: flag-31 handles fail compare"),
    ("m-resshl",   0x3A11D9, db(0x08),
     "shl edx,9 -> 8: resolved id halves"),
    ("m-sel",      0x357095, db(0x02),
     "verb selector sub eax,1 -> 2: arm shift"),
    ("m-mute",     0x3570BE, db(0x74),
     "verb mute jne->je: muted plays, live skipped"),
    ("m-live",     0x267347, db(0x02),
     "liveness test al,1 -> 2: wrong bit"),
    ("m-popdec",   0x267E1A, b"\x90\x90",
     "vmpop dec removed: reads the wrong stack slot"),
    ("m-pushoff",  0x26B4F4, db(0x16),
     "vmpush +0x15 -> +0x16: type written to wrong offset"),
]

def main():
    raw, secs, iat = load_image()
    out = {"exe_sha256": SHA, "cases": [], "mutants": [], "faults": []}
    npass = nfail = 0
    for case in build_cases():
        ret, tr, faults, w, extra = run_case(case, raw, secs, iat)
        ok = (tr == case["want_trace"] and not
              [f for f in faults if f[0] == "MEM"])
        if case["want_ret"] is not None:
            ok = ok and ret == case["want_ret"]
        if "want_push" in case:
            ok = ok and (extra["push_type"], extra["push_val"] & 0xFFFFFFFF) == \
                 (case["want_push"][0], case["want_push"][1])
        npass += ok; nfail += (not ok)
        if not ok:
            print("FAIL %s  ret=%d want=%s\n  got:  %s\n  want: %s\n  push=%s faults=%s"
                  % (case["name"], ret, case["want_ret"], tr,
                     case["want_trace"], extra, faults))
        else:
            print("PASS %s" % case["name"])
        out["cases"].append({"name": case["name"], "ret": ret,
                             "trace": tr, "ok": bool(ok),
                             "calls": w.calls, "extra": extra,
                             "faults": faults})
    print("cases: %d/%d" % (npass, npass + nfail))
    fired = set()
    for case in build_cases():
        ret, tr, faults, w, extra = run_case(case, raw, secs, iat)
        fired |= w.fired
    out["bodies_fired"] = ["0x%X" % v for v in sorted(fired)]
    print("fired:", " ".join("%s@%x" % (CALLS[v], v) for v in sorted(fired)))

    base = {c["name"]: (c["ret"], c["trace"],
                        (c["extra"]["push_type"], c["extra"]["push_val"]))
            for c in out["cases"]}
    for name, va, data, why in MUTANTS:
        n_diff = 0; diffs = []
        for case in build_cases():
            c = dict(case); c["patch_bytes"] = [(va, data)]
            ret, tr, faults, w, extra = run_case(c, raw, secs, iat)
            obs = (ret, tr, (extra["push_type"], extra["push_val"]))
            if obs != base[case["name"]] or \
               [f for f in faults if f[0] == "MEM"]:
                n_diff += 1
                diffs.append((case["name"], "ret=%d tr=%s" % (ret, tr)))
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
