# EXP-109 render-pool-lifecycle-exec
#
# Executes the SHIPPED bytes of the six CharacterRenderSystem lifecycle
# free functions named in CONTRACT-render-record-pool-lifecycle under
# Unicorn, plus every shallow callee that carries contract semantics.
#
#   004269A0  CTOR   pool constructor. 0041F730 CLR x160 records, tail
#             indices, name-table regs (T3W/T2W/T1W), tail config
#             +0x48840..0x4886C, 7 subsystem inits (SLTI/HTI/T3I/T4I/
#             T5I real clears, E0720 -> S512+D40 stubs, S53 globals +
#             E400/E620/E520 stubs), +0x48818|=5, +0x4881C=32.5f,
#             +0x48824=4.0f, +0x48828=0x3E2AAAAB epoch. ret = POOL.
#
#   004278E0  LKUP   rcx=name. Active list: skips records with
#             b[rec+0x290]&2 (retired/hidden). Pending list: no flag
#             gate. hit->u16 id, miss->-1.
#
#   004279B0  ALOC   rcx=name,rdx=buf1,r8=buf2,r9d=flags.
#             LKUP!=-1 -> 0; live>=0xA0 -> 0; i=nextFree; CLR(rec_i);
#             pending append (head==-1->head=i else tail.next=i,prev=
#             old tail); tPend=i; w[rec]=i; RINIT stub (rec,name,buf1,
#             obj=BASE(d[+0x48830]), stack: orig_r8d, orig_r9d);
#             +0x290|=1; live++; nextFree = live>=0xA0 ? 0 : first
#             d[rec+0x284]==0 scanning nextFree+1 wrap. ret rec.
#
#   00428710  PROM   drain pending -> active per rec: PTD stub;
#             +0x414 = +0x48828 epoch; G68 (q[rec+0x400]!=0 -> E56 stub
#             -> b[ret]!=0 -> HID stub(w[rec]) -> +0x114); PHOOK stub
#             with +0x48818 bit0 pinned to pre-call value; +0x290&=~1;
#             unlink pending; append active tail; +0x48818|=0x20;
#             tAct=i. Ends hPend=tPend=-1 always.
#
#   00427C90  RETI   per active rec with b[rec+0x290]&2: unlink;
#             live--; head/tailAct fixups; live==0->nextFree=0;
#             F4C0 stub; drain child chain w[rec+8] via 00426EC0 REAL;
#             +0x114!=0 -> HC1 real (slot-table enable clear);
#             +0x118!=0 -> HC2 real (handle-table clear); TDOWN stub;
#             +0x48818|=0x20. hAct==-1 -> no-op.
#
#   00429140  RELE   rcx=rec. null->0. d[rec+0x284]&4 (retired):
#             +0x290|=2, +0x2AE|=1, +0x108=0, +0x110=0,
#             +0x284=(d&~4)|(1<<30); L2D gate (d[rec+0xC4]!=-1 ->
#             BASE(d[rec+0x10]) -> T51 stub(q[obj+0xDA8],d[rec+0xC4])
#             -> d[rax+0xC]&=~2); d[rec+0x18]!=-1 -> BASE -> MIDS stub
#             (q[obj+0xD98],edi) -> d[rbx]&=~4; BAS2(0) -> +0xA0 write.
#             ret 1.
#             b[rec+0x290]&1 (pending): unlink; live--; head/tailPend
#             fixups; live==0->nextFree=0; CLR; ret 1.
#             else -> ret 1 unchanged.
#
# Real callees: 0041F730 CLR, 0020E600/0020E620 resolvers, 0041D6C0/
#   D0/E0 table writers, 00426EC0 drain, 003B6000/003AFBE0 handle
#   clears, 003E68E0/00422D50 resolver gates, 006C0520, 0046D110->
#   00202C70 (0x40B const copy from shipped 0x1F204E0), 003E5D00,
#   003E37E0, inits 003B6890/003AFCD0/004778A0/003AF2B0/0042F000/
#   003B53C0 (global writes real, subsystem calls scripted).
#
# Scripted boundaries: 00420480 RINIT, 0041FCF0 PTD, 003B56D0 HID,
#   0042C410 PHOOK, 004200A0 TDOWN, 003E56A0, 002ED570 MIDS,
#   0051B9E0 T51, 00512EF0, 0040DB70, 0032E400/620/520,
#   0036C1D0/0036A100/0036C140 allocator trio (unplanted-table
#   paths only), 00861EC0 memset thunk (implemented as real memset —
#   its writes ARE the semantics).
#
import ctypes, hashlib, json, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_RIP, \
    UC_X86_REG_RSP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

CTOR = 0x004269A0
LKUP = 0x004278E0
ALOC = 0x004279B0
PROM = 0x00428710
RETI = 0x00427C90
RELE = 0x00429140

CLR    = 0x0041F730
BASE   = 0x0020E600
BAS2   = 0x0020E620
T1W    = 0x0041D6C0
T2W    = 0x0041D6D0
T3W    = 0x0041D6E0
DRAIN  = 0x00426EC0
HC1    = 0x003B6000
HC2    = 0x003AFBE0
G68    = 0x003E68E0
L2D    = 0x00422D50
F4W    = 0x006C0520
CPY    = 0x0046D110
A8W    = 0x003E5D00
Z50    = 0x003E37E0
SLTI   = 0x003B6890
HTI    = 0x003AFCD0
T3I    = 0x004778A0
T4I    = 0x003AF2B0
T5I    = 0x0042F000
S53    = 0x003B53C0
E0720  = 0x003E0720

RINIT  = 0x00420480
PTD    = 0x0041FCF0
HID    = 0x003B56D0
PHOOK  = 0x0042C410
TDOWN  = 0x004200A0
F4C0   = 0x0042F4C0
E56    = 0x003E56A0
MIDS   = 0x002ED570
T51    = 0x0051B9E0
S512   = 0x00512EF0
D40    = 0x0040DB70
E400   = 0x0032E400
E620   = 0x0032E620
E520   = 0x0032E520
AL1    = 0x0036C1D0
AL2    = 0x0036A100
AL3    = 0x0036C140
MEMSET = 0x00861EC0

G_POOL   = 0x022C6F28
G_BASE   = 0x01F83530
G_SLOTS  = 0x02B40528
G_GATE   = 0x02B40524
G_S520   = 0x02B40520
G_TAB2   = 0x02B3F530
G_TAB2C1 = 0x02B3F538
G_TAB2C2 = 0x02B3F53C
G_TAB2C3 = 0x02B3F540
G_HTAB   = 0x02B3F570
G_HTIC1  = 0x02B3F550
G_HTIC2  = 0x02B3F554
G_HTIB   = 0x02B3F574
G_T3B    = 0x2CA6CA0
G_T3C1   = 0x2CA6C90
G_T3C2   = 0x2CA6C94
G_S53A   = 0x02B4050A
G_S53B   = 0x02B4050C
G_S53C   = 0x02B40508
G_S53D   = 0x02B40514
G_S53E   = 0x02B40510
G_S53F   = 0x02B40512
G_S53G   = 0x02B40518
G_S53STR = 0x02AD9B60
G_T5B    = 0x2CA48D4
G_T5C    = 0x2CA4ED0
G_NAM1   = 0x2CA4410
G_NAM2   = 0x2CA4670
G_NAM3   = 0x2CA4668
CPY_SRC  = 0x01F204E0

POOL   = HEAP + 0x000000
TAIL   = POOL + 0x48800
OBJB   = HEAP + 0x800000
SLOTS  = HEAP + 0x900000
HTAB2  = HEAP + 0xA00000
E56O   = HEAP + 0xB00000
T51O   = HEAP + 0xB10000
MIDO   = HEAP + 0xB20000
BUFN   = HEAP + 0xC00000
NAMEP  = HEAP + 0xD00000
SLOTS2 = HEAP + 0xE00000

NREC = 0xA0
STRIDE = 0x740

# 0041D6C0 (T1W) index -> lea-rdx target, extracted from ctor's 24 call
# sites; T2W idx5 -> 0x520C50; T3W -> 0x1F000A0.
NAM1 = {0x11: 0x520160, 0x15: 0x520740, 0x16: 0x520BD0, 0x13: 0x520430,
        0x12: 0x5207C0, 0x18: 0x520C80, 0x19: 0x520CE0, 0x1A: 0x520C10,
        0x1D: 0x520D30, 0x1E: 0x520DF0, 0x1F: 0x520140, 0x20: 0x5207A0,
        0x21: 0x520780, 0x23: 0x520180, 0x24: 0x5201B0, 0x25: 0x520320,
        0x28: 0x520720, 0x29: 0x520D00, 0x2A: 0x5206B0, 0x14: 0x520E70,
        0x2F: 0x520E30, 0x34: 0x520800, 0x3F: 0x520510, 0x48: 0x5205B0}


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v
def sx16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v


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


def img_rd(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + rs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("image read outside shipped bytes: %x" % va)


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


def _clr_image(raw, secs):
    """post-reset 0x740 record image produced by 0041F730.
    memset + the extracted store list; all xmm6-derived stores are 0
    (const 0x1CEBBA8 == 0.0f) and +0x4C0/+0x580 regions stay zero."""
    img = bytearray(0x740)
    for o in (0x00, 0x02, 0x04, 0x06, 0x08, 0x0A, 0x60, 0x64, 0xCC, 0xCE,
              0x2F8, 0x2F0, 0x40F, 0x408, 0x24C, 0x2C8, 0x2CA, 0x2AC):
        struct.pack_into("<H", img, o, 0xFFFF)
    struct.pack_into("<H", img, 0x4B4, 0x1000)
    img[0x2AF] = 0xFF
    img[0x412] = 0xFF
    img[0x4B7] = 0x20
    img[0x66D] = 0x02
    for o in (0x18, 0xC4, 0xC8, 0x450, 0x2C4, 0x288, 0x434, 0x6A4, 0x718):
        struct.pack_into("<i", img, o, -1)
    for k, fv in enumerate((100.0, 200.0, 300.0, 400.0, 500.0, 600.0,
                            700.0)):
        struct.pack_into("<f", img, 0xA4 + k * 4, fv)
    struct.pack_into("<I", img, 0x2A0, 0xF)
    struct.pack_into("<I", img, 0x2F4, 0x3050303)
    for o in (0x2B0, 0x2B4, 0x2B8):
        struct.pack_into("<f", img, o, -1.0)
    struct.pack_into("<f", img, 0x2BC, 30.0)
    for o, v in ((0x414, 0x3E2AAAAB), (0x41C, 0x3C360B67),
                 (0x420, 0x3C5A72A8), (0x424, 0x3D88888D),
                 (0x428, 0x3E4CCCCD), (0x4B0, 0x3CF5C28F),
                 (0x4A4, 2), (0x738, 1)):
        struct.pack_into("<I", img, o, v)
    for o in (0x12C, 0x13C, 0x14C, 0x15C, 0x160, 0x164, 0x168,
              0x16C, 0x170, 0x174, 0x178, 0x17C, 0x20C, 0x260, 0x264,
              0x268, 0x26C, 0x274, 0x278, 0x27C, 0x280, 0x2A4, 0x31C,
              0x32C, 0x330, 0x334, 0x338, 0x33C, 0x49C, 0x4A8, 0x63C):
        struct.pack_into("<f", img, o, 1.0)
    for o in range(0x210, 0x230, 4):            # F4W x2: 8 x 1.0f
        struct.pack_into("<f", img, o, 1.0)
    for i in range(0xA):                        # A8W: w=0x1000 per slot
        struct.pack_into("<H", img, 0x4C0 + i * 8, 0x1000)
    for o in (0x438, 0x440):
        struct.pack_into("<Q", img, o, 0x0000FFFF0000FFFF)
    src = img_rd(raw, secs, CPY_SRC, 0x40)
    img[0x180:0x1C0] = src
    img[0x1C0:0x200] = src
    return img


def default_rec(i):
    return {"id": i, "prev": 0xFFFF, "next": 0xFFFF, "parent": 0xFFFF,
            "child": 0xFFFF, "sib": 0xFFFF, "d284": 1, "d290": 0,
            "name": "rec%03d" % i, "q400": 0, "d10": 0, "d18": 0xFFFFFFFF,
            "dC4": 0xFFFFFFFF, "d114": 0, "d118": 0}


def _recs(*specs):
    """full 160-entry list, index-ordered, with per-index overrides."""
    recs = [default_rec(i) for i in range(NREC)]
    for spec in specs:
        i = spec.pop("_i")
        recs[i].update(spec)
    return recs


def _w_rec(gm, base, r):
    gm.w(base + 0x00, hw(r.get("id", 0)))
    gm.w(base + 0x02, hw(r.get("prev", 0xFFFF)))
    gm.w(base + 0x04, hw(r.get("next", 0xFFFF)))
    gm.w(base + 0x06, hw(r.get("parent", 0xFFFF)))
    gm.w(base + 0x08, hw(r.get("child", 0xFFFF)))
    gm.w(base + 0x0A, hw(r.get("sib", 0xFFFF)))
    gm.w(base + 0x10, dw(r.get("d10", 0)))
    gm.w(base + 0x18, dw(r.get("d18", 0xFFFFFFFF)))
    gm.w(base + 0xC4, dw(r.get("dC4", 0xFFFFFFFF)))
    gm.w(base + 0xC8, dw(r.get("dC8", 0)))
    gm.w(base + 0x284, dw(r.get("d284", 1)))
    gm.w(base + 0x290, dw(r.get("d290", 0)))
    gm.w(base + 0x2AE, bytes([r.get("b2AE", 0) & 0xFF]))
    gm.w(base + 0x108, qw(r.get("q108", 0)))
    gm.w(base + 0x110, dw(r.get("d110", 0)))
    gm.w(base + 0x114, dw(r.get("d114", 0)))
    gm.w(base + 0x118, dw(r.get("d118", 0)))
    gm.w(base + 0x400, qw(r.get("q400", 0)))
    nm = r.get("name", "")
    if nm:
        gm.w(base + 0x1C, nm.encode() + b"\x00")


def _w_tail(gm, t):
    for name, off in (("hAct", 0x00), ("tAct", 0x04), ("nextFree", 0x08),
                      ("live", 0x0C), ("hPend", 0x10), ("tPend", 0x14),
                      ("flags", 0x18), ("w2c", 0x2C), ("d30", 0x30)):
        if name in t:
            if name == "w2c":
                gm.w(TAIL + off, hw(t[name] & 0xFFFF))
            else:
                gm.w(TAIL + off, dw(t[name] & 0xFFFFFFFF))
    for name, off in (("f1c", 0x1C), ("f24", 0x24), ("epoch", 0x28)):
        if name in t:
            gm.w(TAIL + off, struct.pack("<f", t[name]))


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)

        gm.w(G_POOL, qw(POOL))
        gm.w(G_BASE, qw(OBJB))
        gm.w(G_SLOTS, qw(case.get("slots_tab", SLOTS)))
        gm.w(G_TAB2, qw(case.get("tab2", HTAB2)))
        gm.w(G_GATE, dw(case.get("gate", 0xFFFFFFFF)))
        gm.w(G_S520, dw(case.get("s520", 0xFFFFFFFF)))

        recs = case.get("recs") or [default_rec(i) for i in range(NREC)]
        for i, r in enumerate(recs):
            _w_rec(gm, POOL + i * STRIDE, r)
        _w_tail(gm, case.get("tail", {}))

        # slot table: 0x1C0 stride x 0x50; enable bytes at +0x40/+0x120,
        # identity dwords at +0x10/+0xF0 (HC1 resolves handle via *0xE0)
        stab = case.get("slots_tab", SLOTS)
        if stab:
            for i in range(0x50):
                gm.w(stab + i * 0x1C0 + 0x40,
                     bytes([case.get("slot_b40", 1) & 0xFF]))
                gm.w(stab + i * 0x1C0 + 0x120,
                     bytes([case.get("slot_b40", 1) & 0xFF]))
                gm.w(stab + i * 0x1C0 + 0x10, dw(i))
                gm.w(stab + i * 0x1C0 + 0xF0, dw(i))
            for h, sidx in case.get("hmap", {}).items():
                gm.w(stab + (h & 0xFF) * 0xE0 + 0x10, dw(h))

        for i in range(0x20):
            gm.w(G_HTAB + i * 0x70 + 4, dw(case.get("htab4", 0)))
        for h, eidx in case.get("htab", {}).items():
            gm.w(G_HTAB + (h & 0xFF) * 0x70 + 4, dw(h))

        for i, r in enumerate(recs):
            off = r.get("d10", 0) & 0xFFFFFFFF
            gm.w(OBJB + off + 0xD98, qw(r.get("o_d98", MIDO + i * 0x100)))
            gm.w(OBJB + off + 0xDA8, qw(r.get("o_da8", T51O + i * 0x100)))

        e56o = case.get("e56_obj", E56O)
        gm.w(e56o, bytes([case.get("e56_b0", 1) & 0xFF]))
        gm.w(T51O + 0xC, dw(case.get("t51_c", 0xFF)))
        gm.w(MIDO + 0x0, dw(case.get("mido_0", 0xFF)))
        gm.w(NAMEP, case.get("qname", b"rec000\x00"))

        self.trace, self.faults, self.fired = [], [], set()
        self._stub_n = {}
        for va, data in case.get("plants", []):
            gm.w(va, data)
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (RINIT, PTD, HID, PHOOK, TDOWN, E56, MIDS, T51, S512,
                   D40, E400, E620, E520, AL1, AL2, AL3, MEMSET, F4C0):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        for va in (CLR, BASE, BAS2, T1W, T2W, T3W, DRAIN, HC1, HC2, G68,
                   L2D, SLTI, HTI, T3I, T4I, T5I, S53, LKUP):
            uc.hook_add(UC_HOOK_CODE, self.on_watch, begin=va, end=va)

    def _pop_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RIP, back)

    def _fx(self, key):
        fx = self.case.get("fx", {}).get(key, [])
        n = self._stub_n.get(key, 0) - 1
        seq = fx[n] if 0 <= n < len(fx) else (fx[-1] if fx else [])
        for va, data in seq:
            self.gm.w(va, data)

    def on_watch(self, uc, addr, size, _):
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        if addr == CLR:
            self.trace.append("c%x" % (rcx & 0xFFFFFFFF))
        elif addr == LKUP:
            self.trace.append("L%x" % (rcx & 0xFFFFFFFF))
        elif addr == BASE:
            self.trace.append("e%x" % (rcx & 0xFFFFFFFF))
        elif addr == BAS2:
            self.trace.append("b2")
        elif addr == T1W:
            self.trace.append("1%x" % (rcx & 0xFFFFFFFF))
        elif addr == T2W:
            self.trace.append("2%x" % (rcx & 0xFFFFFFFF))
        elif addr == T3W:
            self.trace.append("3")
        elif addr == DRAIN:
            self.trace.append("d%x" % (rcx & 0xFFFFFFFF))
        elif addr == HC1:
            self.trace.append("H%x" % (rcx & 0xFFFFFFFF))
        elif addr == HC2:
            self.trace.append("j%x" % (rcx & 0xFFFFFFFF))
        elif addr == G68:
            self.trace.append("g%x" % (rcx & 0xFFFFFFFF))
        elif addr == L2D:
            self.trace.append("l%x" % (rcx & 0xFFFFFFFF))
        elif addr == SLTI:
            self.trace.append("S")
        elif addr == HTI:
            self.trace.append("N")
        elif addr == T3I:
            self.trace.append("3i")
        elif addr == T4I:
            self.trace.append("6i")
        elif addr == T5I:
            self.trace.append("5i")
        elif addr == S53:
            self.trace.append("8i")

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        c = self.case
        rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF
        rdx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF
        r8 = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF
        r9 = uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF
        if addr == MEMSET:
            n = r8 & 0xFFFFFFFF
            self.gm.w(rcx, bytes([rdx & 0xFF]) * n)
            self.trace.append("M%x:%x:%x" % (rcx & 0xFFFFFFFF,
                                             rdx & 0xFF, n))
            self._pop_ret()
            return
        key = "%x" % addr
        self._stub_n[key] = self._stub_n.get(key, 0) + 1
        if addr == RINIT:
            sp = uc.reg_read(UC_X86_REG_RSP)
            a5 = struct.unpack("<I", self.gm.r(sp + 0x28, 4))[0]
            a6 = struct.unpack("<I", self.gm.r(sp + 0x30, 4))[0]
            self.trace.append("I%x:%x:%x:%x:%x:%x" % (
                rcx & 0xFFFFFFFF, rdx & 0xFFFFFFFF, r8 & 0xFFFFFFFF,
                r9 & 0xFFFFFFFF, a5, a6))
        elif addr == PTD:
            self.trace.append("t%x" % (rcx & 0xFFFFFFFF))
        elif addr == HID:
            self.trace.append("h%x" % (rcx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX,
                         c.get("hid_ret", 0x100) + self._stub_n[key] - 1)
            self._fx(key)
            self._pop_ret()
            return
        elif addr == PHOOK:
            self.trace.append("p%x" % (rcx & 0xFFFFFFFF))
            self._fx(key)
            self._pop_ret()
            return
        elif addr == F4C0:
            self.trace.append("4%x" % (rcx & 0xFFFFFFFF))
            self._fx(key)
            self._pop_ret()
            return
        elif addr == TDOWN:
            self.trace.append("T%x" % (rcx & 0xFFFFFFFF))
            self._fx(key)
            self._pop_ret()
            return
        elif addr == E56:
            self.trace.append("E%x" % (rcx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, c.get("e56_ret", E56O))
            self._pop_ret()
            return
        elif addr == MIDS:
            self.trace.append("m%x:%x" % (rcx & 0xFFFFFFFF,
                                          rdx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, c.get("mids_ret", MIDO))
            self._pop_ret()
            return
        elif addr == T51:
            self.trace.append("t5%x:%x" % (rcx & 0xFFFFFFFF,
                                           rdx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, c.get("t51_ret", T51O))
            self._pop_ret()
            return
        elif addr == S512:
            self.trace.append("s512")
        elif addr == D40:
            self.trace.append("D40")
        elif addr == E400:
            self.trace.append("e400:%x" % (rcx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, c.get("e400_ret", 0))
            self._pop_ret()
            return
        elif addr == E620:
            self.trace.append("e620:%x:%x:%x" % (
                rcx & 0xFFFFFFFF, r8 & 0xFFFFFFFF, r9 & 0xFFFFFFFF))
        elif addr == E520:
            self.trace.append("e520:%x" % (rcx & 0xFFFFFFFF))
        elif addr == AL1:
            self.trace.append("a1:%x:%x" % (rcx & 0xFFFFFFFF,
                                            rdx & 0xFFFFFFFF))
        elif addr == AL2:
            self.trace.append("a2:%x" % (rcx & 0xFFFFFFFF))
            ret = c.get("al2_ret", SLOTS2 if rcx == 0x8C00 else HTAB2)
            uc.reg_write(UC_X86_REG_RAX, ret)
            self._pop_ret()
            return
        elif addr == AL3:
            self.trace.append("a3")
        self._pop_ret()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


# ---- model ---------------------------------------------------------------

class MPool:
    def __init__(self, case, raw, secs):
        self.case, self.raw, self.secs = case, raw, secs
        recs = case.get("recs") or [default_rec(i) for i in range(NREC)]
        self.recs = [dict(r) for r in recs]
        self.t = dict({"hAct": 0xFFFFFFFF, "tAct": 0xFFFFFFFF,
                       "nextFree": 0, "live": 0, "hPend": 0xFFFFFFFF,
                       "tPend": 0xFFFFFFFF, "flags": 0, "w2c": 0xFFFF,
                       "d30": 0},
                      **{k: v for k, v in case.get("tail", {}).items()})
        self.img = [bytearray(self._rec_bytes(r)) for r in self.recs]
        self._hid_n = 0
        self._phook_n = 0

    def _rec_bytes(self, r):
        img = bytearray(0x740)
        for key, off in (("id", 0), ("prev", 2), ("next", 4),
                         ("parent", 6), ("child", 8), ("sib", 0x0A)):
            struct.pack_into("<H", img, off, r.get(key, 0xFFFF) & 0xFFFF)
        struct.pack_into("<I", img, 0x10, r.get("d10", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", img, 0x18,
                         r.get("d18", 0xFFFFFFFF) & 0xFFFFFFFF)
        struct.pack_into("<I", img, 0xC4,
                         r.get("dC4", 0xFFFFFFFF) & 0xFFFFFFFF)
        struct.pack_into("<I", img, 0x284, r.get("d284", 1) & 0xFFFFFFFF)
        struct.pack_into("<I", img, 0x290, r.get("d290", 0) & 0xFFFFFFFF)
        img[0x2AE] = r.get("b2AE", 0) & 0xFF
        struct.pack_into("<Q", img, 0x108, r.get("q108", 0))
        struct.pack_into("<I", img, 0x110, r.get("d110", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", img, 0x114, r.get("d114", 0) & 0xFFFFFFFF)
        struct.pack_into("<I", img, 0x118, r.get("d118", 0) & 0xFFFFFFFF)
        struct.pack_into("<Q", img, 0x400, r.get("q400", 0))
        nm = r.get("name", "")
        if nm:
            img[0x1C:0x1C + len(nm) + 1] = nm.encode() + b"\x00"
        return img

    def d(self, i, off):
        return struct.unpack_from("<I", self.img[i], off)[0]

    def u16(self, i, off):
        return struct.unpack_from("<H", self.img[i], off)[0]

    def sd(self, i, off, v):
        struct.pack_into("<I", self.img[i], off, v & 0xFFFFFFFF)

    def sw(self, i, off, v):
        struct.pack_into("<H", self.img[i], off, v & 0xFFFF)

    def clr(self, tr, i):
        rva = POOL + i * STRIDE
        tr.append("c%x" % (rva & 0xFFFFFFFF))
        tr.append("M%x:0:740" % (rva & 0xFFFFFFFF))
        tr.append("M%x:0:50" % ((rva + 0x580) & 0xFFFFFFFF))
        self.img[i] = bytearray(_clr_image(self.raw, self.secs))

    def name_of(self, i):
        end = self.img[i].find(b"\x00", 0x1C)
        return bytes(self.img[i][0x1C:end])

    def lookup(self, name):
        idx = s32(self.t["hAct"])
        while idx != -1:
            if not (self.d(idx, 0x290) & 2) and                     self.name_of(idx) == name.encode():
                return idx
            idx = sx16(self.u16(idx, 4))
        idx = s32(self.t["hPend"])
        while idx != -1:
            if self.name_of(idx) == name.encode():
                return idx
            idx = sx16(self.u16(idx, 4))
        return -1

    def alloc(self, name):
        tr = ["L%x" % (NAMEP & 0xFFFFFFFF)]
        if self.lookup(name) != -1:
            return 0, tr
        if s32(self.t["live"]) >= NREC:
            return 0, tr
        i = s32(self.t["nextFree"])
        rva = POOL + i * STRIDE
        self.clr(tr, i)
        if s32(self.t["hPend"]) == -1:
            self.t["hPend"] = i
        else:
            tail = s32(self.t["tPend"])
            self.sw(tail, 4, i)
            self.sw(i, 2, tail)
        self.t["tPend"] = i
        self.sw(i, 0, i)
        ecx = s32(self.t.get("d30", 0))
        tr.append("e%x" % (ecx & 0xFFFFFFFF))
        tr.append("I%x:%x:%x:%x:%x:%x" % (
            rva & 0xFFFFFFFF, NAMEP & 0xFFFFFFFF,
            self.case.get("rdx", BUFN) & 0xFFFFFFFF,
            (OBJB + ecx) & 0xFFFFFFFFFFFFFFFF,
            self.case.get("r8", BUFN + 0x100) & 0xFFFFFFFF,
            self.case.get("r9d", 0) & 0xFFFFFFFF))
        self.sd(i, 0x290, self.d(i, 0x290) | 1)
        self.t["live"] = (s32(self.t["live"]) + 1) & 0xFFFFFFFF
        if s32(self.t["live"]) >= NREC:
            self.t["nextFree"] = 0
        else:
            j = s32(self.t["nextFree"])
            while True:
                j += 1
                self.t["nextFree"] = j & 0xFFFFFFFF
                if j >= NREC:
                    j = 0
                    self.t["nextFree"] = 0
                if self.d(j, 0x284) == 0:
                    break
        return rva, tr

    def prom(self):
        tr = []
        i = s32(self.t["hPend"])
        while i != -1:
            nxt = sx16(self.u16(i, 4))
            rva = POOL + i * STRIDE
            tr.append("t%x" % (rva & 0xFFFFFFFF))
            struct.pack_into("<f", self.img[i], 0x414,
                             self.t.get("epoch", 0.0))
            tr.append("g%x" % (rva & 0xFFFFFFFF))
            if struct.unpack_from("<Q", self.img[i], 0x400)[0] != 0:
                tr.append("E%x" % (rva & 0xFFFFFFFF))
                if self.case.get("e56_ret", E56O) and \
                        self.case.get("e56_b0", 1) & 0xFF:
                    tr.append("h%x" % self.u16(i, 0))
                    hid = self.case.get("hid_ret", 0x100) + self._hid_n
                    self._hid_n += 1
                    self.sd(i, 0x114, hid)
            old = self.t["flags"] & 0xFFFFFFFF
            tr.append("p%x" % (rva & 0xFFFFFFFF))
            fx = self.case.get("fx", {}).get("%x" % PHOOK, [])
            seq = fx[self._phook_n] if self._phook_n < len(fx) else \
                (fx[-1] if fx else [])
            self._phook_n += 1
            for va, data in seq:
                if va == TAIL + 0x18 and len(data) == 4:
                    self.t["flags"] = struct.unpack("<I", data)[0]
            new = self.t["flags"] & 0xFFFFFFFF
            self.t["flags"] = (new & ~1 & 0xFFFFFFFF) | (old & 1)
            self.sd(i, 0x290, self.d(i, 0x290) & ~1 & 0xFFFFFFFF)
            pv, nx = sx16(self.u16(i, 2)), nxt
            if pv != -1:
                self.sw(pv, 4, nx)
            if nx != -1:
                self.sw(nx, 2, pv)
            rid = self.u16(i, 0)
            if s32(self.t["hPend"]) == rid:
                self.t["hPend"] = nx & 0xFFFFFFFF if nx != -1 else \
                    0xFFFFFFFF
            if s32(self.t["tPend"]) == rid:
                self.t["tPend"] = pv & 0xFFFFFFFF if pv != -1 else \
                    0xFFFFFFFF
            if s32(self.t["hAct"]) == -1:
                self.t["hAct"] = i
                self.sw(i, 2, 0xFFFF)
            else:
                ot = s32(self.t["tAct"])
                self.sw(ot, 4, i)
                self.sw(i, 2, ot)
            self.sw(i, 4, 0xFFFF)
            self.t["flags"] = (self.t["flags"] | 0x20) & 0xFFFFFFFF
            self.t["tAct"] = i
            i = nxt
        self.t["hPend"] = 0xFFFFFFFF
        self.t["tPend"] = 0xFFFFFFFF
        return tr

    def drain(self, tr, c):
        """00426EC0 — unlink child c from its parent's +0x8/+0xA chain.
        Every exit except w[c+6]==-1 still writes c's +0x6/+0xA = -1."""
        p = sx16(self.u16(c, 6))
        if p == -1:
            return
        cid = self.u16(c, 0)
        if self.d(p, 0x284) != 0:
            cur = sx16(self.u16(p, 8))
            if cur == cid:
                self.sw(p, 8, self.u16(c, 0x0A))
            else:
                rax_i = cur
                while rax_i != -1 and self.d(rax_i, 0x284) != 0:
                    ns = sx16(self.u16(rax_i, 0x0A))
                    if ns == -1 or ns == cid:
                        break
                    rax_i = ns
                if rax_i != -1 and self.d(rax_i, 0x284) != 0 and \
                        sx16(self.u16(rax_i, 0x0A)) == cid:
                    self.sw(rax_i, 0x0A, self.u16(c, 0x0A))
        self.sw(c, 6, 0xFFFF)
        self.sw(c, 0x0A, 0xFFFF)

    def reti(self, tr, slots_img, htab_img):
        i = s32(self.t["hAct"])
        while i != -1:
            nxt = sx16(self.u16(i, 4))
            if self.d(i, 0x290) & 2:
                rva = POOL + i * STRIDE
                pv = sx16(self.u16(i, 2))
                if pv != -1:
                    self.sw(pv, 4, nxt)
                if nxt != -1:
                    self.sw(nxt, 2, pv)
                self.t["live"] = (s32(self.t["live"]) - 1) & 0xFFFFFFFF
                rid = self.u16(i, 0)
                if s32(self.t["hAct"]) == rid:
                    self.t["hAct"] = nxt & 0xFFFFFFFF if nxt != -1 \
                        else 0xFFFFFFFF
                if s32(self.t["tAct"]) == rid:
                    self.t["tAct"] = pv & 0xFFFFFFFF if pv != -1 \
                        else 0xFFFFFFFF
                if s32(self.t["live"]) == 0:
                    self.t["nextFree"] = 0
                tr.append("4%x" % (rva & 0xFFFFFFFF))
                while True:
                    c = sx16(self.u16(i, 8))
                    if c == -1:
                        break
                    tr.append("d%x" % ((POOL + c * STRIDE) & 0xFFFFFFFF))
                    self.drain(tr, c)
                h1 = self.d(i, 0x114)
                if h1 != 0:
                    tr.append("H%x" % h1)
                    s = h1 * 0xE0
                    if struct.unpack_from("<I", slots_img, s + 0x10)[0] \
                            == h1:
                        slots_img[s + 0x40] &= 0xFE
                h2 = self.d(i, 0x118)
                if h2 != 0:
                    tr.append("j%x" % h2)
                    e = (h2 & 0xFF) * 0x70
                    if struct.unpack_from("<I", htab_img, e + 4)[0] == h2:
                        struct.pack_into("<I", htab_img, e + 4, 0)
                tr.append("T%x" % (rva & 0xFFFFFFFF))
                self.t["flags"] = (self.t["flags"] | 0x20) & 0xFFFFFFFF
            i = nxt
        return tr

    def rele(self, tr, rcx):
        if rcx == 0:
            return 0
        i = (rcx - POOL) // STRIDE
        if self.d(i, 0x284) & 4:
            self.sd(i, 0x290, self.d(i, 0x290) | 2)
            self.img[i][0x2AE] |= 1
            struct.pack_into("<Q", self.img[i], 0x108, 0)
            self.sd(i, 0x110, 0)
            self.sd(i, 0x284,
                    (self.d(i, 0x284) & ~4 & 0xFFFFFFFF) | (1 << 30))
            tr.append("l%x" % (rcx & 0xFFFFFFFF))
            if s32(self.d(i, 0xC4)) != -1:
                ecx = self.d(i, 0x10)
                tr.append("e%x" % ecx)
                tr.append("t5%x:%x" % (
                    self.recs[i].get("o_da8", T51O + i * 0x100)
                    & 0xFFFFFFFFFFFFFFFF, self.d(i, 0xC4)))
            if s32(self.d(i, 0x18)) != -1:
                ecx = self.d(i, 0x10)
                tr.append("e%x" % ecx)
                tr.append("m%x:%x" % (
                    self.recs[i].get("o_d98", MIDO + i * 0x100)
                    & 0xFFFFFFFFFFFFFFFF, self.d(i, 0x18)))
                if self.case.get("mids_ret", MIDO):
                    tr.append("b2")
            return 1
        if self.d(i, 0x290) & 1:
            pv = sx16(self.u16(i, 2))
            nx = sx16(self.u16(i, 4))
            if pv != -1:
                self.sw(pv, 4, nx)
            if nx != -1:
                self.sw(nx, 2, pv)
            self.t["live"] = (s32(self.t["live"]) - 1) & 0xFFFFFFFF
            rid = self.u16(i, 0)
            if s32(self.t["hPend"]) == rid:
                self.t["hPend"] = nx & 0xFFFFFFFF if nx != -1 else \
                    0xFFFFFFFF
            if s32(self.t["tPend"]) == rid:
                self.t["tPend"] = pv & 0xFFFFFFFF if pv != -1 else \
                    0xFFFFFFFF
            if s32(self.t["live"]) == 0:
                self.t["nextFree"] = 0
            self.clr(tr, i)
            return 1
        return 1

    def ctor(self):
        tr = []
        for i in range(NREC):
            self.clr(tr, i)
        self.t.update({"hAct": 0xFFFFFFFF, "tAct": 0xFFFFFFFF,
                       "nextFree": 0, "live": 0, "hPend": 0xFFFFFFFF,
                       "tPend": 0xFFFFFFFF, "flags": 0, "w2c": 0xFFFF})
        tr.append("3")
        tr.append("2%x" % 5)
        for i in (0x11, 0x15, 0x16, 0x13, 0x12, 0x18, 0x19, 0x1A, 0x1D,
                  0x1E, 0x1F, 0x20, 0x21, 0x23, 0x24, 0x25, 0x28, 0x29,
                  0x2A, 0x14, 0x2F, 0x34, 0x3F, 0x48):
            tr.append("1%x" % i)
        tr.append("S")
        if not self.case.get("slots_tab", SLOTS):
            tr += ["a1:6:6", "a2:8c00", "a3"]
        tr.append("N")
        tr.append("3i")
        tr.append("6i")
        if not self.case.get("tab2", HTAB2):
            tr += ["a1:6:6", "a2:3000", "a3"]
        tr.append("5i")
        tr += ["s512", "D40", "8i",
               "e400:9",
               "e620:9:%x:%x" % (G_S53STR & 0xFFFFFFFF,
                                 self.case.get("e400_ret", 0)),
               "e520:0"]
        self.t["flags"] = (self.t["flags"] | 5) & 0xFFFFFFFF
        return tr


# ---- run + compare ---------------------------------------------------------

def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    entry = case.get("entry", CTOR)
    if entry == LKUP:
        uc.reg_write(UC_X86_REG_RCX, NAMEP)
    elif entry == ALOC:
        uc.reg_write(UC_X86_REG_RCX, NAMEP)
        uc.reg_write(UC_X86_REG_RDX, case.get("rdx", BUFN))
        uc.reg_write(UC_X86_REG_R8, case.get("r8", BUFN + 0x100))
        uc.reg_write(UC_X86_REG_R9, case.get("r9d", 0)
                     & 0xFFFFFFFFFFFFFFFF)
    elif entry in (RELE, DRAIN):
        uc.reg_write(UC_X86_REG_RCX, case.get("rcx", 0)
                     & 0xFFFFFFFFFFFFFFFF)
    try:
        uc.emu_start(entry, RETQ, count=4_000_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))

    gm = w.gm
    obs = {"ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF}
    for name, off in (("hAct", 0), ("tAct", 4), ("nextFree", 8),
                      ("live", 0x0C), ("hPend", 0x10), ("tPend", 0x14),
                      ("flags", 0x18), ("w2c", 0x2C), ("d30", 0x30)):
        obs[name] = struct.unpack("<I", gm.r(TAIL + off, 4))[0]
    obs["f1c"] = struct.unpack("<f", gm.r(TAIL + 0x1C, 4))[0]
    obs["f24"] = struct.unpack("<f", gm.r(TAIL + 0x24, 4))[0]
    obs["epoch"] = struct.unpack("<f", gm.r(TAIL + 0x28, 4))[0]
    watch = case.get("watch", [])
    obs["recs"] = []
    for i in watch:
        b = POOL + i * STRIDE
        obs["recs"].append([
            i,
            struct.unpack("<H", gm.r(b + 0, 2))[0],
            struct.unpack("<H", gm.r(b + 2, 2))[0],
            struct.unpack("<H", gm.r(b + 4, 2))[0],
            struct.unpack("<H", gm.r(b + 6, 2))[0],
            struct.unpack("<H", gm.r(b + 8, 2))[0],
            struct.unpack("<H", gm.r(b + 0x0A, 2))[0],
            struct.unpack("<I", gm.r(b + 0x284, 4))[0],
            struct.unpack("<I", gm.r(b + 0x290, 4))[0],
            gm.r(b + 0x2AE, 1)[0],
            struct.unpack("<I", gm.r(b + 0x114, 4))[0],
            struct.unpack("<I", gm.r(b + 0x118, 4))[0],
            struct.unpack("<f", gm.r(b + 0x414, 4))[0],
        ])
    if case.get("full_rec"):
        obs["recfull"] = list(gm.r(POOL + case["full_rec"] * STRIDE,
                                   0x740))
    # handle/slot side effects
    stab = case.get("slots_tab", SLOTS) or \
        case.get("al2_ret", SLOTS2)
    obs["hc1"] = [[h, gm.r(stab + (h & 0xFF) * 0xE0 + 0x40, 1)[0]]
                  for h in case.get("hmap", {})]
    obs["hc2"] = [[h, struct.unpack("<I", gm.r(
        G_HTAB + (h & 0xFF) * 0x70 + 4, 4))[0]]
                  for h in case.get("htab", {})]
    obs["t51o_c"] = struct.unpack("<I", gm.r(T51O + 0xC, 4))[0]
    obs["mido_0"] = struct.unpack("<I", gm.r(MIDO, 4))[0]
    obs["mido_a0"] = struct.unpack("<I", gm.r(MIDO + 0xA0, 4))[0]
    if entry == CTOR:
        obs["g_slots"] = struct.unpack("<Q", gm.r(G_SLOTS, 8))[0]
        obs["gate"] = struct.unpack("<I", gm.r(G_GATE, 4))[0]
        obs["s520"] = struct.unpack("<I", gm.r(G_S520, 4))[0]
        obs["htic1"] = struct.unpack("<I", gm.r(G_HTIC1, 4))[0]
        obs["htic2"] = struct.unpack("<I", gm.r(G_HTIC2, 4))[0]
        obs["htib0"] = struct.unpack("<I", gm.r(G_HTIB, 4))[0]
        obs["htib31"] = struct.unpack("<I", gm.r(G_HTIB + 31 * 0x70, 4))[0]
        obs["t3c1"] = struct.unpack("<I", gm.r(G_T3C1, 4))[0]
        obs["t3c2"] = struct.unpack("<Q", gm.r(G_T3C2, 8))[0]
        obs["t3w0"] = struct.unpack("<H", gm.r(G_T3B, 2))[0]
        obs["t3w31"] = struct.unpack("<H", gm.r(G_T3B + 31 * 0x40, 2))[0]
        obs["t5c"] = struct.unpack("<I", gm.r(G_T5C, 4))[0]
        obs["t5d0"] = struct.unpack("<I", gm.r(G_T5B, 4))[0]
        obs["t2"] = struct.unpack("<Q", gm.r(G_TAB2, 8))[0]
        obs["t2c1"] = struct.unpack("<I", gm.r(G_TAB2C1, 4))[0]
        obs["t2c2"] = struct.unpack("<I", gm.r(G_TAB2C2, 4))[0]
        obs["t2c3"] = struct.unpack("<I", gm.r(G_TAB2C3, 4))[0]
        t2 = case.get("tab2", HTAB2) or case.get("al2_ret", HTAB2)
        obs["t4b0"] = gm.r(t2, 1)[0]
        obs["t4b127"] = gm.r(t2 + 127 * 0x60, 1)[0]
        obs["nam3"] = struct.unpack("<Q", gm.r(G_NAM3, 8))[0]
        obs["nam2_5"] = struct.unpack("<Q", gm.r(G_NAM2 + 5 * 8, 8))[0]
        for i in (0x11, 0x2A, 0x48):
            obs["nam1_%x" % i] = struct.unpack(
                "<Q", gm.r(G_NAM1 + i * 8, 8))[0]
        obs["s53a"] = gm.r(G_S53A, 1)[0]
        obs["s53b"] = struct.unpack("<I", gm.r(G_S53B, 4))[0]
        obs["s53c"] = struct.unpack("<H", gm.r(G_S53C, 2))[0]
        obs["s53d"] = struct.unpack("<I", gm.r(G_S53D, 4))[0]
        obs["s53e"] = struct.unpack("<H", gm.r(G_S53E, 2))[0]
        obs["s53f"] = gm.r(G_S53F, 1)[0]
        obs["s53g"] = gm.r(G_S53G, 1)[0]
        obs["t40"] = struct.unpack("<H", gm.r(TAIL + 0x40, 2))[0]
        obs["t42"] = gm.r(TAIL + 0x42, 1)[0]
        obs["t43"] = gm.r(TAIL + 0x43, 1)[0]
        obs["t4c"] = struct.unpack("<I", gm.r(TAIL + 0x4C, 4))[0]
        obs["t50"] = struct.unpack("<I", gm.r(TAIL + 0x50, 4))[0]
        obs["t54"] = struct.unpack("<I", gm.r(TAIL + 0x54, 4))[0]
        obs["t58"] = struct.unpack("<I", gm.r(TAIL + 0x58, 4))[0]
        obs["t5c"] = struct.unpack("<I", gm.r(TAIL + 0x5C, 4))[0]
        obs["t60"] = struct.unpack("<I", gm.r(TAIL + 0x60, 4))[0]
        obs["t64"] = struct.unpack("<Q", gm.r(TAIL + 0x64, 8))[0]
        obs["t6c"] = struct.unpack("<I", gm.r(TAIL + 0x6C, 4))[0]
        stab2 = case.get("slots_tab", SLOTS) or \
            case.get("al2_ret", SLOTS2)
        obs["sl_b40"] = gm.r(stab2 + 0x40, 1)[0]
        obs["sl_b120"] = gm.r(stab2 + 0x120, 1)[0]
    return " ".join(w.trace) or "-", w.faults, obs


def _exp_tail(mp):
    t = mp.t
    return {k: v & 0xFFFFFFFF for k, v in
            ((n, s32(t[n])) for n in
             ("hAct", "tAct", "nextFree", "live", "hPend", "tPend",
              "flags", "w2c", "d30"))}


def _exp_recs(mp, watch):
    out = []
    for i in watch:
        im = mp.img[i]
        out.append([
            i,
            struct.unpack_from("<H", im, 0)[0],
            struct.unpack_from("<H", im, 2)[0],
            struct.unpack_from("<H", im, 4)[0],
            struct.unpack_from("<H", im, 6)[0],
            struct.unpack_from("<H", im, 8)[0],
            struct.unpack_from("<H", im, 0x0A)[0],
            struct.unpack_from("<I", im, 0x284)[0],
            struct.unpack_from("<I", im, 0x290)[0],
            im[0x2AE],
            struct.unpack_from("<I", im, 0x114)[0],
            struct.unpack_from("<I", im, 0x118)[0],
            struct.unpack_from("<f", im, 0x414)[0],
        ])
    return out


def _empty_tail():
    return {"hAct": 0xFFFFFFFF, "tAct": 0xFFFFFFFF, "nextFree": 0,
            "live": 0, "hPend": 0xFFFFFFFF, "tPend": 0xFFFFFFFF,
            "flags": 0, "w2c": 0xFFFF, "d30": 0}


def build_cases():
    C = []

    def A(name, **kw):
        C.append(dict(name=name, **kw))

    # ---- LKUP ----
    base = _recs({"_i": 2, "d290": 0, "prev": 0xFFFF, "next": 5},
                 {"_i": 5, "d290": 0, "prev": 2, "next": 9},
                 {"_i": 9, "d290": 0, "prev": 5, "next": 0xFFFF},
                 {"_i": 20, "d290": 1, "prev": 0xFFFF, "next": 40},
                 {"_i": 40, "d290": 1, "prev": 20, "next": 0xFFFF})
    lk_tail = dict(_empty_tail(), hAct=2, tAct=9, hPend=20, tPend=40,
                   live=5, nextFree=3)
    A("lkup-active-head", entry=LKUP, qname=b"rec002\x00", recs=base,
      tail=lk_tail)
    A("lkup-active-mid", entry=LKUP, qname=b"rec005\x00", recs=base,
      tail=lk_tail)
    A("lkup-active-tail", entry=LKUP, qname=b"rec009\x00", recs=base,
      tail=lk_tail)
    A("lkup-pending", entry=LKUP, qname=b"rec040\x00", recs=base,
      tail=lk_tail)
    A("lkup-miss", entry=LKUP, qname=b"ghost\x00", recs=base,
      tail=lk_tail)
    A("lkup-invisible", entry=LKUP, qname=b"rec007\x00",
      recs=_recs({"_i": 7, "d290": 2, "name": "rec007"}),
      tail=dict(_empty_tail(), hAct=7, tAct=7, live=1))
    A("lkup-empty", entry=LKUP, qname=b"rec000\x00", tail=_empty_tail())

    # ---- ALOC ----
    A("aloc-first", entry=ALOC,
      tail=dict(_empty_tail(), d30=5, epoch=0.25), qname=b"new1\x00",
      watch=[0])
    A("aloc-second", entry=ALOC,
      recs=_recs({"_i": 0, "d290": 1, "name": "first"}),
      tail=dict(_empty_tail(), hPend=0, tPend=0, live=1, nextFree=1),
      qname=b"new2\x00", watch=[0, 1])
    A("aloc-mid", entry=ALOC,
      recs=_recs({"_i": 0, "prev": 0xFFFF, "next": 3, "d290": 2},
                 {"_i": 3, "prev": 0, "next": 0xFFFF, "d290": 2},
                 {"_i": 7, "d290": 1, "name": "p1"}),
      tail=dict(_empty_tail(), hAct=0, tAct=3, hPend=7, tPend=7,
                live=3, nextFree=5),
      qname=b"new3\x00", watch=[0, 3, 5, 7])
    A("aloc-exists", entry=ALOC, recs=base, tail=lk_tail,
      qname=b"rec005\x00")
    A("aloc-exists-pend", entry=ALOC, recs=base, tail=lk_tail,
      qname=b"rec020\x00")
    A("aloc-full", entry=ALOC, tail=dict(_empty_tail(), live=0xA0),
      qname=b"new4\x00")
    A("aloc-lastfree", entry=ALOC,
      tail=dict(_empty_tail(), live=0x9F, nextFree=0x9F),
      qname=b"new5\x00", watch=[0x9F])
    A("aloc-third", entry=ALOC,
      recs=_recs({"_i": 0, "next": 3, "d290": 1, "name": "p1"},
                 {"_i": 3, "prev": 0, "d290": 1, "name": "p2"}),
      tail=dict(_empty_tail(), hPend=0, tPend=3, live=2, nextFree=5),
      qname=b"new6\x00", watch=[0, 3, 5])
    A("aloc-pendempty", entry=ALOC,
      recs=_recs({"_i": 0, "d290": 0, "name": "a"}),
      tail=dict(_empty_tail(), hAct=0, tAct=0, live=1, nextFree=5),
      qname=b"new7\x00", watch=[0, 5])
    A("aloc-scanwrap", entry=ALOC,
      tail=dict(_empty_tail(), live=0x9E, nextFree=0x9E),
      qname=b"new8\x00", watch=[0x9E])

    # ---- PROM ----
    A("prom-empty", entry=PROM, tail=_empty_tail())
    A("prom-single", entry=PROM,
      recs=_recs({"_i": 4, "d290": 1, "name": "p"}),
      tail=dict(_empty_tail(), hPend=4, tPend=4, live=1, epoch=0.25),
      watch=[4])
    A("prom-multi", entry=PROM,
      recs=_recs({"_i": 1, "prev": 0xFFFF, "next": 5, "d290": 1,
                  "name": "x"},
                 {"_i": 5, "prev": 1, "next": 8, "d290": 1, "name": "y",
                  "q400": E56O},
                 {"_i": 8, "prev": 5, "next": 0xFFFF, "d290": 1,
                  "name": "z"},
                 {"_i": 2, "d290": 2, "name": "a"}),
      tail=dict(_empty_tail(), hAct=2, tAct=2, hPend=1, tPend=8,
                live=4, flags=2, epoch=0.16666667),
      watch=[1, 2, 5, 8])
    A("prom-nohandle", entry=PROM,
      recs=_recs({"_i": 4, "d290": 1, "name": "p", "q400": E56O}),
      tail=dict(_empty_tail(), hPend=4, tPend=4, live=1, epoch=0.25),
      e56_b0=0, watch=[4])
    A("prom-pinbit1", entry=PROM,
      recs=_recs({"_i": 4, "d290": 1, "name": "p"}),
      tail=dict(_empty_tail(), hPend=4, tPend=4, live=1, flags=0),
      fx={"%x" % PHOOK: [[(TAIL + 0x18, dw(0x63))]]}, watch=[4])
    A("prom-staleprev", entry=PROM,
      recs=_recs({"_i": 5, "prev": 3, "next": 0xFFFF, "d290": 1},
                 {"_i": 3, "prev": 7, "next": 9}),
      tail=dict(_empty_tail(), hPend=5, tPend=5, live=1),
      watch=[3, 5])
    A("prom-bit0pin", entry=PROM,
      recs=_recs({"_i": 4, "d290": 1, "name": "p"}),
      tail=dict(_empty_tail(), hPend=4, tPend=4, live=1, flags=0),
      fx={"%x" % PHOOK: [[(TAIL + 0x18, dw(0x61))]]}, watch=[4])

    # ---- RETI ----
    A("reti-empty", entry=RETI, tail=_empty_tail())
    A("reti-none", entry=RETI,
      recs=_recs({"_i": 2, "prev": 0xFFFF, "next": 5, "d290": 0},
                 {"_i": 5, "prev": 2, "next": 9, "d290": 0},
                 {"_i": 9, "prev": 5, "next": 0xFFFF, "d290": 0}),
      tail=dict(_empty_tail(), hAct=2, tAct=9, live=3),
      watch=[2, 5, 9])
    A("reti-all", entry=RETI,
      recs=_recs({"_i": 2, "prev": 0xFFFF, "next": 5, "d290": 2},
                 {"_i": 5, "prev": 2, "next": 9, "d290": 2},
                 {"_i": 9, "prev": 5, "next": 0xFFFF, "d290": 2}),
      tail=dict(_empty_tail(), hAct=2, tAct=9, live=3, nextFree=4),
      watch=[2, 5, 9])
    A("reti-one", entry=RETI,
      recs=_recs({"_i": 2, "prev": 0xFFFF, "next": 5, "d290": 0},
                 {"_i": 5, "prev": 2, "next": 9, "d290": 2, "d114": 7,
                  "d118": 3, "q400": E56O},
                 {"_i": 9, "prev": 5, "next": 0xFFFF, "d290": 0}),
      tail=dict(_empty_tail(), hAct=2, tAct=9, live=3, nextFree=4),
      hmap={7: 7}, htab={3: 3}, watch=[2, 5, 9])
    A("reti-children", entry=RETI,
      recs=_recs({"_i": 2, "d290": 3, "child": 11},
                 {"_i": 11, "parent": 2, "sib": 12, "id": 11},
                 {"_i": 12, "parent": 2, "sib": 13, "id": 12},
                 {"_i": 13, "parent": 2, "sib": 0xFFFF, "id": 13}),
      tail=dict(_empty_tail(), hAct=2, tAct=2, live=4, nextFree=4),
      watch=[2, 11, 12, 13])
    A("drain-mid", entry=DRAIN, rcx=POOL + 12 * STRIDE,
      recs=_recs({"_i": 20, "child": 21},
                 {"_i": 21, "parent": 20, "sib": 12, "child": 30},
                 {"_i": 30, "parent": 21},
                 {"_i": 12, "parent": 20}),
      tail=_empty_tail(), watch=[12, 20, 21, 30])
    A("reti-head-tail", entry=RETI,
      recs=_recs({"_i": 2, "prev": 0xFFFF, "next": 5, "d290": 2},
                 {"_i": 5, "prev": 2, "next": 9, "d290": 0},
                 {"_i": 9, "prev": 5, "next": 0xFFFF, "d290": 0}),
      tail=dict(_empty_tail(), hAct=2, tAct=9, live=3, nextFree=4),
      watch=[2, 5, 9])
    A("reti-tail-flag", entry=RETI,
      recs=_recs({"_i": 2, "prev": 0xFFFF, "next": 5, "d290": 0},
                 {"_i": 5, "prev": 2, "next": 9, "d290": 0},
                 {"_i": 9, "prev": 5, "next": 0xFFFF, "d290": 2}),
      tail=dict(_empty_tail(), hAct=2, tAct=9, live=3, nextFree=4),
      watch=[2, 5, 9])

    # ---- RELE ----
    A("rele-null", entry=RELE, rcx=0, tail=_empty_tail())
    A("rele-active", entry=RELE, rcx=POOL + 5 * STRIDE,
      recs=_recs({"_i": 5, "d290": 2}),
      tail=dict(_empty_tail(), hAct=5, tAct=5, live=1), watch=[5])
    A("rele-pending", entry=RELE, rcx=POOL + 5 * STRIDE,
      recs=_recs({"_i": 5, "d290": 1}),
      tail=dict(_empty_tail(), hPend=5, tPend=5, live=1, nextFree=9),
      watch=[5])
    A("rele-pending-mid", entry=RELE, rcx=POOL + 5 * STRIDE,
      recs=_recs({"_i": 3, "prev": 0xFFFF, "next": 5, "d290": 1},
                 {"_i": 5, "prev": 3, "next": 8, "d290": 1},
                 {"_i": 8, "prev": 5, "next": 0xFFFF, "d290": 1}),
      tail=dict(_empty_tail(), hPend=3, tPend=8, live=3, nextFree=9),
      watch=[3, 5, 8])
    A("rele-pending-head", entry=RELE, rcx=POOL + 3 * STRIDE,
      recs=_recs({"_i": 3, "prev": 0xFFFF, "next": 5, "d290": 1},
                 {"_i": 5, "prev": 3, "next": 8, "d290": 1},
                 {"_i": 8, "prev": 5, "next": 0xFFFF, "d290": 1}),
      tail=dict(_empty_tail(), hPend=3, tPend=8, live=3, nextFree=9),
      watch=[3, 5, 8])
    A("rele-pending-tail", entry=RELE, rcx=POOL + 8 * STRIDE,
      recs=_recs({"_i": 3, "prev": 0xFFFF, "next": 5, "d290": 1},
                 {"_i": 5, "prev": 3, "next": 8, "d290": 1},
                 {"_i": 8, "prev": 5, "next": 0xFFFF, "d290": 1}),
      tail=dict(_empty_tail(), hPend=3, tPend=8, live=3, nextFree=9),
      watch=[3, 5, 8])
    A("rele-retired", entry=RELE, rcx=POOL + 5 * STRIDE,
      recs=_recs({"_i": 5, "d284": 0x44, "d290": 0, "d10": 0x40,
                  "d18": 7, "dC4": 9}),
      tail=dict(_empty_tail(), live=1), watch=[5])
    A("rele-retired-c4neg", entry=RELE, rcx=POOL + 5 * STRIDE,
      recs=_recs({"_i": 5, "d284": 0x44, "d290": 0, "d10": 0x40,
                  "d18": 7, "dC8": 0x55}),
      tail=dict(_empty_tail(), live=1), watch=[5])
    A("rele-retired-nomids", entry=RELE, rcx=POOL + 5 * STRIDE,
      recs=_recs({"_i": 5, "d284": 0x44, "d290": 0, "d10": 0x40,
                  "d18": 7, "dC4": 9}),
      tail=dict(_empty_tail(), live=1), mids_ret=0, watch=[5])
    A("rele-retired-neg1", entry=RELE, rcx=POOL + 5 * STRIDE,
      recs=_recs({"_i": 5, "d284": 0x44, "d290": 0}),
      tail=dict(_empty_tail(), live=1), watch=[5])

    # ---- CTOR ----
    A("ctor-fresh", entry=CTOR, watch=[0, 1, 2], full_rec=3)
    A("ctor-rec120", entry=CTOR, watch=[120], full_rec=120)
    A("ctor-allocpath", entry=CTOR, slots_tab=0, tab2=0, watch=[0])

    return C


def _slots_img(case):
    img = bytearray(0x50 * 0x1C0)
    for i in range(0x50):
        img[i * 0x1C0 + 0x40] = case.get("slot_b40", 1)
        img[i * 0x1C0 + 0x120] = case.get("slot_b40", 1)
        struct.pack_into("<I", img, i * 0x1C0 + 0x10, i)
        struct.pack_into("<I", img, i * 0x1C0 + 0xF0, i)
    for h in case.get("hmap", {}):
        struct.pack_into("<I", img, (h & 0xFF) * 0xE0 + 0x10, h)
    return img


def _htab_img(case):
    img = bytearray(0x20 * 0x70)
    for i in range(0x20):
        struct.pack_into("<I", img, i * 0x70 + 4, case.get("htab4", 0))
    for h in case.get("htab", {}):
        struct.pack_into("<I", img, (h & 0xFF) * 0x70 + 4, h)
    return img


def main():
    raw, secs = load_image()
    cases = build_cases()
    npass = 0
    results = {"exe_sha256": SHA, "cases": [], "mutants": []}
    for case in cases:
        tr, faults, obs = run_case(case, raw, secs)
        mp = MPool(case, raw, secs)
        entry = case.get("entry", CTOR)
        name = case.get("qname", b"").rstrip(b"\x00").decode()
        watch = case.get("watch", [])
        exp, mtr = {}, ""
        if entry == LKUP:
            exp["ret"] = mp.lookup(name) & 0xFFFFFFFF
            mtr = "L%x" % (NAMEP & 0xFFFFFFFF)
        elif entry == ALOC:
            exp["ret"], tl = mp.alloc(name)
            mtr = " ".join(tl)
            exp.update(_exp_tail(mp))
            exp["recs"] = _exp_recs(mp, watch)
        elif entry == PROM:
            mtr = " ".join(mp.prom())
            exp.update(_exp_tail(mp))
            exp["recs"] = _exp_recs(mp, watch)
        elif entry == RETI:
            si, hi = _slots_img(case), _htab_img(case)
            tl = []
            mtr = " ".join(mp.reti(tl, si, hi))
            exp.update(_exp_tail(mp))
            exp["recs"] = _exp_recs(mp, watch)
            exp["hc1"] = [[h, struct.unpack_from(
                "<B", si, (h & 0xFF) * 0xE0 + 0x40)[0]]
                for h in case.get("hmap", {})]
            exp["hc2"] = [[h, struct.unpack_from(
                "<I", hi, (h & 0xFF) * 0x70 + 4)[0]]
                for h in case.get("htab", {})]
        elif entry == DRAIN:
            rcx = case.get("rcx", 0)
            ri = (rcx - POOL) // STRIDE if rcx else -1
            tl = ["d%x" % (rcx & 0xFFFFFFFF)]
            mp.drain(tl, ri)
            mtr = " ".join(tl)
            exp["ret"] = 0xFFFFFFFF
            exp["recs"] = _exp_recs(mp, watch)
        elif entry == RELE:
            tl = []
            rcx = case.get("rcx", 0)
            ri = (rcx - POOL) // STRIDE if rcx else -1
            retired = ri >= 0 and (mp.d(ri, 0x284) & 4) != 0
            dc4 = s32(mp.d(ri, 0xC4)) if ri >= 0 else -1
            d18 = s32(mp.d(ri, 0x18)) if ri >= 0 else -1
            exp["ret"] = mp.rele(tl, rcx)
            mtr = " ".join(tl)
            exp.update(_exp_tail(mp))
            exp["recs"] = _exp_recs(mp, watch)
            exp["t51o_c"] = (case.get("t51_c", 0xFF) & ~2) & 0xFFFFFFFF \
                if retired and dc4 != -1 and case.get("t51_ret", T51O) \
                else case.get("t51_c", 0xFF)
            midr = case.get("mids_ret", MIDO)
            exp["mido_0"] = (case.get("mido_0", 0xFF) & ~4) & 0xFFFFFFFF \
                if retired and d18 != -1 and midr \
                else case.get("mido_0", 0xFF)
            exp["mido_a0"] = (-OBJB) & 0xFFFFFFFF \
                if retired and d18 != -1 and midr else 0
        elif entry == CTOR:
            tl = mp.ctor()
            mtr = " ".join(tl)
            exp["ret"] = POOL
            exp.update(_exp_tail(mp))
            exp["recs"] = _exp_recs(mp, watch)
            stab = case.get("slots_tab", SLOTS) or \
                case.get("al2_ret", SLOTS2)
            exp["g_slots"] = stab
            exp["gate"] = 0
            exp["s520"] = 0
            exp["htic1"] = 0
            exp["htic2"] = 1
            exp["htib0"] = 0
            exp["htib31"] = 0
            exp["t3c1"] = 0
            exp["t3c2"] = 0
            exp["t3w0"] = 0
            exp["t3w31"] = 0
            exp["t5c"] = 0
            exp["t5d0"] = 0
            exp["t2"] = case.get("tab2", HTAB2) or \
                case.get("al2_ret", HTAB2)
            exp["t2c1"] = 0
            exp["t2c2"] = 0
            exp["t2c3"] = 0
            exp["t4b0"] = 0
            exp["t4b127"] = 0
            exp["nam3"] = 0x1F000A0
            exp["nam2_5"] = 0x520C50
            for i in (0x11, 0x2A, 0x48):
                exp["nam1_%x" % i] = NAM1[i]
            exp["s53a"] = 0
            exp["s53b"] = 0xFFFFFFFF
            exp["s53c"] = 0
            exp["s53d"] = 0xFFFFFFFF
            exp["s53e"] = 0
            exp["s53f"] = 0
            exp["s53g"] = 0
            exp["t40"] = 0
            exp["t42"] = 1
            exp["t43"] = 0
            exp["t4c"] = 0
            exp["t50"] = 4
            exp["t54"] = 0x80404040
            exp["t58"] = 0x40
            exp["t5c"] = 0x40
            exp["t60"] = 0
            exp["t64"] = 0x40A00000
            exp["t6c"] = 0x3F800000
            exp["sl_b40"] = 0
            exp["sl_b120"] = 0
            exp["f1c"] = 34.0
            exp["f24"] = 4.0
            exp["epoch"] = struct.unpack(
                "<f", struct.pack("<I", 0x3E2AAAAB))[0]
        if case.get("full_rec"):
            exp["recfull"] = list(_clr_image(raw, secs))
        errs = []
        if (tr if tr != "-" else "") != mtr:
            errs.append("trace\n  obs: %s\n  exp: %s" % (tr, mtr))
        if faults:
            errs.append("faults: %s" % (faults[:3],))
        for k in exp:
            if obs.get(k) != exp[k]:
                errs.append("%s\n  obs: %s\n  exp: %s"
                            % (k, obs.get(k), exp[k]))
        status = "PASS" if not errs else "FAIL"
        if not errs:
            npass += 1
        print("%-22s %s  ret=%x  %s" % (case["name"], status,
                                       obs["ret"], tr[:80]))
        for e in errs[:8]:
            print("   ", e.replace("\n", "\n    "))
        results["cases"].append({"name": case["name"], "ok": not errs})
    print("cases: %d/%d" % (npass, len(cases)))
    results["case_count"] = [npass, len(cases)]
    nkilled, mres = run_mutants(raw, secs)
    results["mutants"] = mres
    results["mutant_count"] = [nkilled, len(mres)]
    with open("result.json", "w") as fp:
        json.dump(results, fp, indent=1)




# ---- mutants ---------------------------------------------------------------
# (name, va, orig_byte, patch_byte, discriminating case)
MUTS = [
    # LKUP — flag gate, list heads, link fields, hit/miss
    ("m-lk-flagmsk", 0x427912, 0x02, 0x01, "lkup-invisible"),
    ("m-lk-astride", 0x427906, 0x40, 0x41, "lkup-active-mid"),
    ("m-lk-ahead",   0x4278F2, 0x00, 0x10, "lkup-active-mid"),
    ("m-lk-phead",   0x427948, 0x10, 0x00, "lkup-pending"),
    ("m-lk-anext",   0x42793E, 0x04, 0x02, "lkup-active-mid"),
    ("m-lk-pnext",   0x42798C, 0x04, 0x06, "lkup-pending"),
    ("m-lk-skipcc",  0x427913, 0x75, 0x74, "lkup-active-mid"),
    ("m-lk-hitcc",   0x427937, 0x74, 0x75, "lkup-active-mid"),
    ("m-lk-miss",    0x427995, 0xFF, 0x00, "lkup-miss"),
    # ALOC — gates, list append, fields, free scan
    ("m-al-livecmp", 0x4279EF, 0xA0, 0xA1, "aloc-full"),
    ("m-al-livecell",0x4279EB, 0x0C, 0x08, "aloc-full"),
    ("m-al-nfcell",  0x4279FD, 0x08, 0x0C, "aloc-mid"),
    ("m-al-stride",  0x427A09, 0x40, 0x41, "aloc-mid"),
    ("m-al-pheadcmp",0x427A1A, 0x10, 0x00, "aloc-pendempty"),
    ("m-al-tailw",   0x427A2C, 0x14, 0x10, "aloc-third"),
    ("m-al-nextw",   0x427A3B, 0x04, 0x02, "aloc-third"),
    ("m-al-prevw",   0x427A46, 0x02, 0x04, "aloc-third"),
    ("m-al-tpend",   0x427A49, 0x14, 0x10, "aloc-second"),
    ("m-al-idw",     0x427A4F, 0x37, 0x77, "aloc-first"),
    ("m-al-rinitarg",0x427A52, 0x30, 0x28, "aloc-first"),
    ("m-al-flagor",  0x427A7C, 0x01, 0x02, "aloc-first"),
    ("m-al-liveinc", 0x427A81, 0x0C, 0x08, "aloc-second"),
    ("m-al-scanbound",0x427ABA,0xA0, 0xA1, "aloc-scanwrap"),
    ("m-al-scanfield",0x427AD6,0x84, 0x90, "aloc-mid"),
    ("m-al-scancc",  0x427ADA, 0x75, 0x74, "aloc-mid"),
    ("m-al-wrapcc",  0x427ABE, 0x7C, 0x7D, "aloc-mid"),
    # PROM — epoch, handle, flag pin, unlink, append, final
    ("m-pr-epoc",    0x428775, 0x14, 0x10, "prom-multi"),
    ("m-pr-epochsrc",0x42876C, 0x28, 0x24, "prom-multi"),
    ("m-pr-hidfld",  0x42878C, 0x14, 0x18, "prom-multi"),
    ("m-pr-flagpin", 0x4287A0, 0xFE, 0xFD, "prom-multi"),
    ("m-pr-xormsk",  0x4287B6, 0x01, 0x03, "prom-pinbit1"),
    ("m-pr-pendclr", 0x4287C3, 0xFE, 0xFD, "prom-multi"),
    ("m-pr-prevunlink",0x4287E1,0x04, 0x02, "prom-staleprev"),
    ("m-pr-aappend", 0x428852, 0x04, 0x02, "prom-multi"),
    ("m-pr-flagor",  0x428869, 0x20, 0x10, "prom-multi"),
    ("m-pr-endhp",   0x428896, 0x10, 0x00, "prom-multi"),
    ("m-pr-endtp",   0x42888F, 0x14, 0x04, "prom-multi"),
    ("m-g68-400",    0x3E68E7, 0x00, 0x08, "prom-nohandle"),
    # RETI — flag, saved-next, live, fixups, children, handles
    ("m-rt-flagmsk", 0x427CD3, 0x02, 0x01, "reti-one"),
    ("m-rt-nextsave",0x427CD7, 0x04, 0x02, "reti-all"),
    ("m-rt-livedec", 0x427D1A, 0x0C, 0x08, "reti-one"),
    ("m-rt-headfix", 0x427D23, 0x00, 0x10, "reti-head-tail"),
    ("m-rt-tailfix", 0x427D38, 0x04, 0x14, "reti-tail-flag"),
    ("m-rt-nfzero",  0x427D52, 0x08, 0x0C, "reti-all"),
    ("m-rt-child",   0x427D61, 0x08, 0x0A, "reti-children"),
    ("m-rt-h1fld",   0x427D8F, 0x14, 0x18, "reti-one"),
    ("m-rt-h2fld",   0x427D9E, 0x18, 0x14, "reti-one"),
    ("m-rt-flagor",  0x427DB9, 0x20, 0x10, "reti-one"),
    # DRAIN — parent/child/sibling field offsets
    ("m-dr-parent",  0x426EC3, 0x06, 0x04, "reti-children"),
    ("m-dr-child",   0x426F00, 0x08, 0x0A, "reti-children"),
    ("m-dr-sib",     0x426F46, 0x0A, 0x08, "drain-mid"),
    # HC1/HC2 — strides and identity fields
    ("m-hc1-stride", 0x3B6006, 0xE0, 0xE1, "reti-one"),
    ("m-hc1-fld",    0x3B6013, 0x10, 0x14, "reti-one"),
    ("m-hc1-and",    0x3B6018, 0x40, 0x41, "reti-one"),
    ("m-hc2-stride", 0x3AFBE6, 0x70, 0x71, "reti-one"),
    ("m-hc2-fld",    0x3AFBF5, 0x04, 0x08, "reti-one"),
    # RELE — null gate, retired mask, field writes, pending unlink
    ("m-rl-nullcc",  0x429153, 0x75, 0x74, "rele-null"),
    ("m-rl-retmsk",  0x429163, 0x04, 0x02, "rele-retired"),
    ("m-rl-flagor",  0x429175, 0x02, 0x01, "rele-retired"),
    ("m-rl-2ae",     0x42917A, 0xAE, 0xAF, "rele-retired"),
    ("m-rl-284and",  0x429194, 0xFB, 0xF7, "rele-retired"),
    ("m-rl-284op",   0x429198, 0x1E, 0x1F, "rele-retired"),
    ("m-rl-pendmsk", 0x42920A, 0x01, 0x02, "rele-pending"),
    ("m-rl-pendhead",0x429258, 0x10, 0x00, "rele-pending-head"),
    ("m-rl-pendtail",0x42926D, 0x14, 0x04, "rele-pending-tail"),
    ("m-rl-nfzero",  0x42928A, 0x08, 0x0C, "rele-pending"),
    ("m-rl-livecmp", 0x42927F, 0x0C, 0x08, "rele-pending"),
    ("m-l2d-c4",     0x422D58, 0xC4, 0xC8, "rele-retired-c4neg"),
    # BASE/BAS2 resolvers
    ("m-base-add",   0x20E603, 0x03, 0x2B, "aloc-first"),
    ("m-bas2-sub",   0x20E620, 0x2B, 0x03, "rele-retired"),
    # CTOR + CLR
    ("m-ct-count",   0x4269D2, 0x01, 0x02, "ctor-rec120"),
    ("m-ct-hact",    0x4269E3, 0x00, 0x10, "ctor-fresh"),
    ("m-ct-flagor",  0x426C5F, 0x05, 0x04, "ctor-fresh"),
    ("m-ct-epoch",   0x426C7B, 0xAB, 0xAC, "ctor-fresh"),
    ("m-ct-t3w",     0x4269DB, 0xC1, 0xC2, "ctor-fresh"),
    ("m-cl-memsz",   0x41F74D, 0x40, 0x3F, "ctor-fresh"),
    ("m-cl-linkfld", 0x41F774, 0x02, 0x04, "ctor-fresh"),
    ("m-cl-a4",      0x41F7D0, 0xA4, 0xA8, "ctor-fresh"),
    ("m-cl-450",     0x41F83B, 0x50, 0x54, "ctor-fresh"),
]


def _obs_diff(base, mut):
    keys = set(base) | set(mut)
    return sorted(k for k in keys if base.get(k) != mut.get(k))


def run_mutants(raw, secs):
    byname = {c["name"]: c for c in build_cases()}
    killed = 0
    out = []
    for name, va, orig, patch, cname in MUTS:
        case = byname[cname]
        # verify shipped byte
        real = img_rd(raw, secs, va, 1)[0]
        if real != orig:
            print("%-16s BADSITE va=%x orig=%02x file=%02x"
                  % (name, va, orig, real))
            out.append({"name": name, "killed": False, "bad_site": True})
            continue
        btr, bf, bobs = run_case(case, raw, secs)
        mcase = dict(case)
        mcase["patch_bytes"] = [(va, bytes([patch]))]
        mtr, mf, mobs = run_case(mcase, raw, secs)
        diff = _obs_diff(bobs, mobs)
        tr_diff = btr != mtr
        f_diff = bool(bf) != bool(mf) or             (bf and mf and bf[0] != mf[0])
        dead = bool(diff) or tr_diff or f_diff
        if dead:
            killed += 1
            why = "obs:%s" % ",".join(diff[:4]) if diff else                   ("trace" if tr_diff else "fault")
        else:
            why = "SURVIVED"
        print("%-16s %-9s case=%s %s" % (name, "KILLED" if dead
                                       else "ALIVE", cname, why))
        out.append({"name": name, "killed": dead})
    print("mutants: %d/%d killed" % (killed, len(MUTS)))
    return killed, out


if __name__ == "__main__":
    main()
