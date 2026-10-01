#!/usr/bin/env python
"""EXP-105 sound-request-fork-exec: execute the Seb/Sep fork residual
flagged by EXP-096 -- the request path past dispatcher 001DBDB0.

Subjects (all shipped bytes under Unicorn):
  00210C00  FORK   two-way selector branch; request path pins sel=0
  0021B5B0  SEB    Seb dispatch: bucket = floor(id/512) on elem+0x3C
  00219EA0  SEP    Sep dispatch: raw id match on elem+0x38
  00212950  RCAL   receipt allocator (counter++, mask 0x7fffffff, 0->1)
  00224540/00224570  Seb worker: tree lower_bound + voice reuse/fresh
  00223160/00223190  Sep worker: voice alloc + flag byte

Both dispatches ALWAYS return a fresh receipt; playback is the
conditional half.  The voice ctor 002255C0 writes +0x1C=0x7F and
+0x20=0x40 (the contract's volume/pan defaults) and the volume setter
002257E0 clamps+writes voice+0x1C directly.

Real bodies (~40): fork + both dispatches + RCAL + both workers + the
leaf setters 00225580-002257E0 + voice ctor 002255C0 + pool pops
002204A0/00220550 + freelist 0016D6D0/0016DA60 + map insert 00199DB0 +
list walkers 00221D10-00222280 + sweeps 00212910/00210A60 + locks
005CD450/005CD4F0/005CD820 (real on planted mutexes) + cookie 00808C40.

Scripted boundaries (disclosed):
  0x7a* STL/shared_ptr carriers (7A6DB0 copy plants dst ptr + local
  flag; 7A7010/7A78B0/7A8CF0 case-controlled returns; 7A7A20 reset;
  7A5A00/7A8060/7A81F0/7A87C0/7A7E00/7A7E90 inside stubbed arms and
  the PAN/VOL tails) -- all entry-intercepted.
  005CC930/005CCB80 spin-wait: only runs when elem+0x30==1 (never in
  these fixtures); intercepted ret-0 if reached.
  00221xxx attach arms 00221940/00221C70: scripted stubs (~at/~ac) --
  the bus-attach closure is a separate contract's subject.
  Deleter/vtable entries: planted scratch bodies (mov eax,imm; ret /
  mov rax,imm64; ret) in mapped memory, disclosed.

EXE: FFXII_TZA.exe sha256 73461d08..721f8, image base 0x120000.
"""
import ctypes, hashlib, json, struct, sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000
HEAP, STACK, RETQ, IMG32 = 0x40000000, 0x60000000, 0x62000000, 0x50000000

# ---- subjects -------------------------------------------------------------
FORK  = 0x00210C00          # Seb/Sep fork (35B)
SEB   = 0x0021B5B0          # Seb dispatch (144B)
SEP   = 0x00219EA0          # Sep dispatch (~156B)
RCAL  = 0x00212950          # receipt allocator (28B)
WSHIM = 0x00224540          # Seb worker arg shim
WSEB  = 0x00224570          # Seb worker (209 insns)
PSHIM = 0x00223160          # Sep worker arg shim
WSEP  = 0x00223190          # Sep worker (~90 insns)

# ---- hooked real bodies ----------------------------------------------------
NOOP  = 0x0016D6A0          # shipped ret-0 no-op ('d')
GET2  = 0x00210B30          # context2 getter ('c', ret-watch)
XREF  = 0x00210710          # refusal virtual check ('x', ret-watch)
COOKIE = 0x00808C40         # stack-cookie check (silent)
S580  = 0x00225580          # voice+0x18 = receipt  ('W18')
S590  = 0x00225590          # voice+0x10 = state    ('W10')
S6A0  = 0x002256A0          # read voice+0x14       ('R14')
S6B0  = 0x002256B0          # voice+0x14 = -1       ('RST')
S6E0  = 0x002256E0          # voice+0x2C = kind     ('W2c')
S6F0  = 0x002256F0          # pan setter            ('PAN')
S7C0  = 0x002257C0          # voice+0x24 = id       ('W24')
S7D0  = 0x002257D0          # voice+0x14 = slot     ('W14')
S7E0  = 0x002257E0          # volume setter         ('VOL')
S670  = 0x00225670          # read voice+0x2C       ('R2c')
S680  = 0x00225680          # read voice+0x10       ('T10')
S690  = 0x00225690          # read voice+0x24       ('R24')

# ---- quiet bodies (real exec, one entry token) ------------------------------
Q_L   = 0x00221D10          # lazy [elem+0x20] init         ('~l')
Q_A   = 0x00221D60          # voice alloc (pool pop+splice) ('~a')
Q_E   = 0x00221E00          # get-or-alloc voice for slot   ('~e')
Q_F1  = 0x00221E60          # find voice by slot (B chain)  ('~f1')
Q_F2  = 0x00221F40          # find voice by id   (B chain)  ('~f2')
Q_SW  = 0x00222280          # sweep+free dead voices        ('~sw')
Q_O   = 0x00222050          # sweep both lists              ('~o')
Q_VC  = 0x002255C0          # voice ctor                    ('~vc')
QUIET = {Q_L: "l", Q_A: "a", Q_E: "e", Q_F1: "f1", Q_F2: "f2",
         Q_SW: "sw", Q_O: "o", Q_VC: "vc"}

# ---- scripted stubs ---------------------------------------------------------
SPIN  = 0x005CC930          # elem+0x30==1 wait fence
SPIN2 = 0x005CCB80          # second fence in the wait loop
T6D   = 0x007A6DB0          # shared_ptr copy (plants dst+flag)
T70   = 0x007A7010          # refcount read -> eax
T78   = 0x007A78B0          # weak lock/validity -> eax
T7A   = 0x007A7A20          # shared_ptr reset
T8C   = 0x007A8CF0          # polymorphic bounds/contains -> al
T5A   = 0x007A5A00          # inside ~at
T80   = 0x007A8060          # inside ~at
T81   = 0x007A81F0          # inside ~at + VOL tail
T87   = 0x007A87C0          # inside ~ac
TE0   = 0x007A7E00          # inside PAN
TE9   = 0x007A7E90          # inside PAN
AT    = 0x00221940          # bus-attach arm A (callback path)
AC    = 0x00221C70          # bus-attach arm B
TD6D  = 0x0016D6D0          # pool tree extract (STL util)
TDA6  = 0x0016DA60          # pool tree relink  (STL util)
TM99  = 0x00199DB0          # std::map insert   (STL util)
QSTUBS = {SPIN: "spin", SPIN2: "spn2", T6D: "s6d", T70: "s70",
          T78: "s78", T7A: "s7a", T8C: "s8c", T5A: "s5a", T80: "s80",
          T81: "s81", T87: "s87", TE0: "se0", TE9: "se9",
          AT: "at", AC: "ac", TD6D: "d6d", TDA6: "da6", TM99: "m99"}

# ---- globals ---------------------------------------------------------------
G_RCPT = 0x01FD36B4         # RCAL counter
G_VCTX = 0x01FD4138         # 221710's voice-context singleton
G_C2   = 0x01FD36A0         # 210b30's context2
G_LST  = 0x01FD4140         # second 222280 sweep list (221e00/222050)

# ---- fixture layout ---------------------------------------------------------
BANK   = HEAP + 0x000000    # fork's rcx: {+8:SEBC, +0x10:SEPC}
SEBC   = HEAP + 0x100000    # Seb sub-controller {+8:listhead}
SEPC   = HEAP + 0x180000    # Sep sub-controller {+8:listhead}
ELEM   = HEAP + 0x200000    # Seb elem (tree voices)
ELEM2  = HEAP + 0x280000    # Sep elem (list voices)
BNODE  = HEAP + 0x300000    # dispatch list node {+0:next,+0x10:elem}
TNODE  = HEAP + 0x380000    # voice tree node {+0:L,+8:R,+0x20:key,+0x28:sd}
SD     = HEAP + 0x400000    # slot descriptor {+4:flags,+9:writebyte}
VOICE  = HEAP + 0x480000    # voice object
VCTX   = HEAP + 0x500000    # voice context (G_VCTX target)
CTX2   = HEAP + 0x580000    # context2 (G_C2 target)
DEL    = HEAP + 0x600000    # deleter obj {+0x10:alloc,+0x18:free fn ptrs}
LNODE  = HEAP + 0x680000    # alloc'd list node returned by deleter alloc
FNODE  = HEAP + 0x700000    # pool freelist node {+0:next,+0x20:voice}
PSUB   = HEAP + 0x780000    # pool+0x50 sub-obj {+0x18:free fn ptr}
VTAB   = HEAP + 0x800000    # planted vtables
SCR    = HEAP + 0x880000    # scratch stub bodies (mov eax,imm; ret)
OBJA   = HEAP + 0x900000    # 210710 objA ([CTX2+0x10])
OBJB   = HEAP + 0x980000    # 210710 objB ([CTX2+8])

QSTUBS[SCR] = "vt"          # planted vtail bodies -> ~vt=<rv>

HOOKS = {RCAL: "n", NOOP: "d", GET2: "c", XREF: "x", COOKIE: "K",
         S580: "W18", S590: "W10", S6A0: "R14", S6B0: "RST",
         S6E0: "W2c", S6F0: "PAN", S7C0: "W24", S7D0: "W14",
         S7E0: "VOL", S670: "R2c", S680: "T10", S690: "R24"}


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
    return raw, secs


def img(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + vs:
            return raw[ra + rva - sva: ra + rva - sva + n]
    raise KeyError("va %x not in image" % va)


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


def fields(base, spec, w):
    for off, v in spec.get("b", {}).items():  w(base + off, bytes([v & 0xFF]))
    for off, v in spec.get("h", {}).items():  w(base + off, hw(v))
    for off, v in spec.get("d", {}).items():  w(base + off, dw(v))
    for off, v in spec.get("f", {}).items():  w(base + off, struct.pack("<f", v))
    for off, v in spec.get("q", {}).items():  w(base + off, qw(v))


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.planted = {}
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(IMG32, 0x400000)
        gm.map(STACK, 0x100000)

        def w(addr, data):
            gm.w(addr, data)
            for i, b in enumerate(data):
                self.planted[addr + i] = b
        self.w = w

        g = case.get("globals", {})

        # ---- the fork's bank object ----
        w(BANK + 8, qw(case.get("sebc", SEBC)))
        w(BANK + 0x10, qw(case.get("sepc", SEPC)))

        # ---- Seb dispatch list (circular, node {+0:next,+0x10:elem}) ----
        seb_elems = case.get("seb_elems", [])
        if seb_elems:
            prev = SEBC + 8
            for i, el in enumerate(seb_elems):
                node = BNODE + i * 0x20
                w(prev, qw(node))
                w(node + 0x10, qw(el))
                prev = node
            w(prev, qw(SEBC + 8))         # last.next -> head
        else:
            w(SEBC + 8, qw(SEBC + 8))     # empty self-loop

        # ---- Sep dispatch list (same shape, match on elem+0x38) ----
        sep_elems = case.get("sep_elems", [])
        if sep_elems:
            prev = SEPC + 8
            for i, el in enumerate(sep_elems):
                node = BNODE + 0x800 + i * 0x20
                w(prev, qw(node))
                w(node + 0x10, qw(el))
                prev = node
            w(prev, qw(SEPC + 8))
        else:
            w(SEPC + 8, qw(SEPC + 8))

        # ---- voice objects ----
        self.voices = {}
        for name, spec in case.get("voices", {}).items():
            va = {"voice": VOICE, "voice2": VOICE + 0x8000}[name]
            self.voices[name] = va
            fields(va, spec, w)

        # ---- Seb elem: {+0:vtab,+0x20:lazy,+0x30:state,+0x3C:bucket,
        #      +0x50:flag,+0x60:sentinel,+0x70:root,+8/+0x10/+0x18 list} ----
        es = case.get("elem", {})
        w(ELEM + 0, qw(VTAB))                    # vtable (vtail +0x50)
        w(VTAB + 0x50, qw(SCR))                  # tail virtual -> ret0
        w(ELEM + 0x20, qw(es.get("lazy", 0)))
        w(ELEM + 0x30, dw(es.get("state", 0)))
        w(ELEM + 0x3C, dw(es.get("bucket", 0)))
        w(ELEM + 0x50, qw(es.get("f50", 0)))
        # voice tree: sentinel at +0x60, root ptr at +0x70
        root = es.get("root", 0)
        w(ELEM + 0x70, qw(root))
        # elem+8 sub-object {+0:first,+8:last,+0x10:deleter}
        vlist = es.get("vlist", [])
        if vlist:
            nodes = []
            for i, va in enumerate(vlist):
                nd = LNODE + 0x400 + i * 0x20
                nodes.append(nd)
                w(nd + 0x10, qw(self.voices.get(va, va)))
            for i, nd in enumerate(nodes):
                nxt = nodes[i + 1] if i + 1 < len(nodes) else ELEM + 8
                prv = nodes[i - 1] if i else ELEM + 8
                w(nd + 0, qw(nxt))
                w(nd + 8, qw(prv))
            w(ELEM + 8, qw(nodes[0]))
            w(ELEM + 0x10, qw(nodes[-1]))
        else:
            w(ELEM + 8, qw(ELEM + 8))
            w(ELEM + 0x10, qw(ELEM + 8))
        w(ELEM + 0x18, qw(DEL))

        # tree node fixture (single node when root set)
        tn = es.get("tnode")
        if tn:
            w(TNODE + 0, qw(0))
            w(TNODE + 8, qw(0))
            w(TNODE + 0x20, dw(tn.get("key", 0)))
            w(TNODE + 0x28, qw(tn.get("sd", SD)))
            w(ELEM + 0x70, qw(TNODE))
        sds = es.get("sd", {})
        fields(SD, sds, w)

        # ---- Sep elem: {+0:vtab,+0x30:state,+0x38:id,+0x44:flags,
        #      +8/+0x10/+0x18 same list trio} ----
        ps = case.get("elem2", {})
        w(ELEM2 + 0, qw(VTAB + 0x100))
        w(VTAB + 0x100 + 0x50, qw(SCR))
        w(ELEM2 + 0x30, dw(ps.get("state", 0)))
        w(ELEM2 + 0x38, dw(ps.get("key", 0)))
        w(ELEM2 + 0x44, bytes([ps.get("flags", 0)]))
        w(ELEM2 + 8, qw(ELEM2 + 8))
        w(ELEM2 + 0x10, qw(ELEM2 + 8))
        w(ELEM2 + 0x18, qw(DEL))

        # ---- deleter: member fn ptrs at +0x10 (alloc) / +0x18 (free) ----
        w(DEL + 0x10, qw(SCR + 0x10))            # -> mov rax,LNODE; ret
        w(DEL + 0x18, qw(SCR + 0x20))            # -> xor eax; ret
        w(SCR + 0x10, b"\x48\xb8" + qw(LNODE) + b"\xc3")
        w(SCR + 0x20, b"\x31\xc0\xc3")
        w(SCR + 0x00, b"\x31\xc0\xc3")           # vtail ret0
        # LNODE defaults (221d60 splices it onto elem+8 list)
        w(LNODE + 0, qw(0))
        w(LNODE + 8, qw(0))
        w(LNODE + 0x10, qw(0))

        # ---- voice context (221710 -> G_VCTX) ----
        w(G_VCTX, qw(VCTX))
        # pool A at VCTX+0xA0 (220d30->220550 pop) and pool B at
        # VCTX+8 (220ce0->2204a0 pop for 221d10's lazy init):
        # {+0x28:copydst,+0x30:freelist,+0x48:count,+0x50:sub,+0x58:map}
        for base, fnode, psub, pvoice, want in (
                (VCTX + 0xA0, FNODE, PSUB, VOICE,
                 case.get("voice_alloc")),
                (VCTX + 8, FNODE + 0x800, PSUB + 0x800, VOICE + 0x8000,
                 case.get("elem", {}).get("lazy", 0) == 0)):
            w(base + 0x48, dw(1 if want else 0))
            if want:
                w(base + 0x30, qw(fnode))
                w(fnode + 0, qw(0))
                w(fnode + 0x20, qw(pvoice))
            w(base + 0x50, qw(psub))
            w(psub + 0x18, qw(SCR + 0x20))       # free fn -> ret0
            w(base + 0x58 + 0x18, qw(0))         # map root null
            w(base + 0x58 + 8, qw(0))            # head
        # ctx+0x300/+0x350 mutexes: zeroed = unlocked (5CD450/5CD820)
        # ctx+0x1D0: 221220's release arg target -- zeroed

        # ---- context2 (210b30 -> G_C2) + 210710 objects ----
        w(G_C2, qw(CTX2))
        w(CTX2 + 8, qw(OBJB))
        w(CTX2 + 0x10, qw(OBJA))
        w(CTX2 + 0x18, qw(CTX2 + 0x18))          # 212910 self-loops
        w(CTX2 + 0x20, qw(CTX2 + 0x20))
        w(CTX2 + 0x28, qw(CTX2 + 0x28))
        w(OBJA + 0, qw(VTAB + 0x200))
        w(OBJB + 0, qw(VTAB + 0x300))
        w(OBJA + 8, qw(OBJA + 8))            # 212910 list self-loops
        w(OBJB + 8, qw(OBJB + 8))
        xa = g.get("xref_a", 0)
        xb = g.get("xref_b", 0)
        w(VTAB + 0x200 + 0x10, qw(SCR + 0x30))
        w(VTAB + 0x300 + 0x10, qw(SCR + 0x40))
        w(SCR + 0x30, b"\xb8" + dw(xa) + b"\xc3")   # mov eax,xa; ret
        w(SCR + 0x40, b"\xb8" + dw(xb) + b"\xc3")

        # ---- second sweep list (221e00/222050 global) ----
        w(G_LST, qw(G_LST))
        w(G_LST + 0x10, qw(DEL))

        # ---- receipt counter ----
        w(G_RCPT, dw(g.get("rcpt", 0)))

        # ---- case-provided extra objects ----
        for addr, spec in case.get("objs", {}).items():
            fields(addr, spec, w)

        self.trace, self.faults, self.fired = [], [], set()
        self.quiet = 0
        self._spn2 = 0
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (list(HOOKS) + list(QUIET) + list(QSTUBS)):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        if self.quiet:
            # hooked tokens suppressed; scripted boundaries still fire
            if addr in QSTUBS:
                self._qstub(uc, addr)
            return
        if addr in QSTUBS:
            rv = self._qstub(uc, addr)
            self.trace.append("~%s=%d" % (QSTUBS[addr], s32(rv)))
            return
        if addr in QUIET:
            self.trace.append("~%s%x" % (QUIET[addr],
                              rcx & 0xFFFFFFFFFFFFFFFF))
            self._quiet_enter()
            return
        if addr == NOOP:
            self.trace.append("d")
        elif addr == COOKIE:
            pass
        elif addr == SCR:
            self.trace.append("~vt")      # vtable tail stub (fixture code)
        elif addr == RCAL:
            self.trace.append("n")
            self._watch_ret()
        elif addr in (GET2, XREF):
            self.trace.append(HOOKS[addr])
            self._watch_ret()
        elif addr in (S580, S590, S6B0, S6E0, S7C0, S7D0):
            self.trace.append("%s%x" % (HOOKS[addr],
                              rcx & 0xFFFFFFFFFFFFFFFF))
        elif addr in (S6A0, S670, S680, S690):
            self.trace.append("%s%x" % (HOOKS[addr],
                              rcx & 0xFFFFFFFFFFFFFFFF))
            self._watch_ret()
        elif addr in (S6F0, S7E0):
            self.trace.append("%s%x" % (HOOKS[addr],
                              rdx & 0xFFFFFFFF))
            self._watch_ret()
        else:
            self.trace.append(HOOKS[addr])
            self._watch_ret()

    # stub return defaults: T8C is the slot-bounds check that passes in
    # every non-bounds-fail fixture
    STUB_DEF = {T8C: 1}

    def _qstub(self, uc, addr):
        """Scripted boundary: emulate disclosed semantics, pop the call."""
        q = self.case.get("qret", {})
        rv = q.get(addr, self.STUB_DEF.get(addr, 0))
        if addr == T6D:
            # shared_ptr copy: dst gets src's ptr; dst+0x110 flag byte
            dst = uc.reg_read(UC_X86_REG_RDX)
            src = uc.reg_read(UC_X86_REG_RCX)
            p = struct.unpack("<Q", self.gm.r(src, 8))[0]
            uc.mem_write(dst, qw(p))
            uc.mem_write(dst + 0x110, bytes([q.get("s6d_flag", 0)]))
        elif addr == TM99:
            # std::map insert: out-pair {ptr,bool} at r8 (result unused
            # by the pool pops -- bookkeeping only)
            r8 = uc.reg_read(UC_X86_REG_R8)
            uc.mem_write(r8, qw(PSUB + 0x400))
            uc.mem_write(r8 + 8, b"\x01")
        elif addr in (SPIN, SPIN2):
            # mixer-wait fence: emulate the mixer having processed the
            # elem -- the real body blocks until elem+0x30 != 1.
            # 224570 keeps elem in rdi, 223190 in rbx.
            if addr == SPIN:
                ns = q.get("spin_state", 0)
            else:
                seq = q.get("spn2_states", [0])
                ns = seq[min(self._spn2, len(seq) - 1)]
                self._spn2 += 1
            for reg in (UC_X86_REG_RDI, UC_X86_REG_RBX):
                p = uc.reg_read(reg)
                if HEAP <= p < HEAP + 0x1000000:
                    uc.mem_write(p + 0x30, dw(ns))
                    break
        self._stub(rv)
        return rv

    def _quiet_enter(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        want = sp + 8
        self.quiet += 1

        def on_ret(uc_, a, s, _u):
            if uc_.reg_read(UC_X86_REG_RSP) != want:
                return
            self.quiet -= 1

        uc.hook_add(UC_HOOK_CODE, on_ret, begin=back, end=back)

    def _stub(self, ret):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RAX, ret & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RIP, back)

    def _watch_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        want = sp + 8
        idx = len(self.trace) - 1
        holder = {"fired": False}

        def on_ret(uc_, a, s, _u):
            if holder["fired"]:
                return
            if uc_.reg_read(UC_X86_REG_RSP) != want:
                return
            holder["fired"] = True
            self.trace[idx] += "=%d" % s32(uc_.reg_read(UC_X86_REG_RAX))

        uc.hook_add(UC_HOOK_CODE, on_ret, begin=back, end=back)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


class Fx:
    def __init__(self, planted):
        self.p = planted
    def b(self, a):   return self.p.get(a, 0)
    def h(self, a):   return self.b(a) | (self.b(a + 1) << 8)
    def d(self, a):   return self.h(a) | self.h(a + 2) << 16
    def q(self, a):   return self.d(a) | self.d(a + 4) << 32


# ---- model -----------------------------------------------------------------

class M:
    def __init__(self, w):
        self.w = w
        self.t = []
        self.obs = []
        self.qret = {}

    def emit(self, s):
        self.t.append(s)
        return len(self.t) - 1
    def done(self, i, r):
        self.t[i] += "=%d" % s32(r)
        return r

    def m_rcal(self):
        """00212950: counter++, &0x7fffffff, zero->1, store, return."""
        i = self.emit("n")
        c = (self.w.d(G_RCPT) + 1) & 0x7FFFFFFF
        if c == 0:
            c = 1
        self.obs.append((G_RCPT, 4, c))
        return self.done(i, c)

    def _seb_list(self, sebc):
        """Yield elem ptrs from the circular dispatch list."""
        out, node, head = [], self.w.q(sebc + 8), sebc + 8
        while node and node != head and len(out) < 16:
            out.append(self.w.q(node + 0x10))
            node = self.w.q(node)
        return out

    def m_seb(self, sebc, snd_id, pan, vol):
        """0021B5B0: bucket=trunc(id/512); receipt always; worker on hit."""
        i32 = s32(snd_id)
        bucket = (i32 + (0x1FF if i32 < 0 else 0)) >> 9
        rcpt = self.m_rcal()
        hit = None
        for el in self._seb_list(sebc):
            if self.w.d(el + 0x3C) == (bucket & 0xFFFFFFFF):
                hit = el
                break
        if hit is not None:
            self.m_wseb(hit, rcpt, snd_id, pan, vol)
        return rcpt

    def m_sep(self, sepc, snd_id, pan, vol):
        """00219EA0: raw-id match on elem+0x38; d token on hit; worker."""
        hit = None
        node, head = self.w.q(sepc + 8), sepc + 8
        while node and node != head:
            el = self.w.q(node + 0x10)
            if el and self.w.d(el + 0x38) == (snd_id & 0xFFFFFFFF):
                hit = el
                break
            node = self.w.q(node)
        rcpt = self.m_rcal()
        if hit is not None:
            self.emit("d")                    # NOOP(ecx = state==2)
            self.m_wsep(hit, rcpt, snd_id, pan, vol)
        return rcpt

    def _s8c(self):
        return self.qret.get(T8C, 1)

    def _spin(self, elem):
        """5cc930 entry + loop 5ccb80 + 5cc930 exit; stubs clear state."""
        self.emit("~spin=%d" % self.qret.get(SPIN, 0))
        if self.qret.get("spin_state", 0) == 1:
            for s in self.qret.get("spn2_states", [0]):
                self.emit("~spn2=%d" % self.qret.get(SPIN2, 0))
                if s != 1:
                    break
        self.emit("~spin=%d" % self.qret.get(SPIN, 0))

    def m_wseb(self, elem, rcpt, snd_id, pan, vol):
        """00224570: tree lower_bound -> sd; reuse/fresh voice arms."""
        w = self.w
        if w.d(elem + 0x30) == 1:
            self._spin(elem)
        slot = snd_id & 0x1FF
        sid = (snd_id | 0x80000000) & 0xFFFFFFFF
        self.emit("d")                        # NOOP(elem+0x50 != 0)
        # lower_bound(elem+0x60 tree, slot): sentinel +0x60, root +0x70
        rax = self._tree_lb(elem + 0x60, slot)
        if rax == elem + 0x60:
            return                            # miss -> silent exit
        sd = w.q(rax + 0x28)
        self.emit("~l%x" % (elem & 0xFFFFFFFFFFFFFFFF))
        lazy = w.q(elem + 0x20)
        if lazy == 0:
            # 220ce0 -> 2204a0(vctx+8) pool-B pop: count--, pop fnodeB's
            # payload, store at elem+0x20 (helpers stubbed, silent)
            lazy = w.q(FNODE + 0x800 + 0x20)
            self.obs.append((VCTX + 8 + 0x48, 4,
                             w.d(VCTX + 8 + 0x48) - 1))
            self.obs.append((elem + 0x20, 8, lazy))
        s8c = self._s8c()
        self.emit("~s8c=%d" % s8c)
        if not s8c:
            return
        b4 = w.b(sd + 4)
        if b4 & 8:
            self.emit("~f2%x" % (elem & 0xFFFFFFFFFFFFFFFF))
            found = self._bfind(elem, (sid & 0xFFFFFE00) + 7, 0x24)
            if slot != 7 and found:
                return
        if b4 & 0x20:
            ic = self.emit("c")
            self.emit("d")                # 210b30 calls 16d6a0 inside
            self.done(ic, CTX2)
            ix = self.emit("x")
            xr = self._xref()
            self.done(ix, xr)
            if xr:
                return
        self.emit("~e%x" % (elem & 0xFFFFFFFFFFFFFFFF))
        voice = self._get_voice(elem, slot)
        iT = self.emit("T10%x" % (voice & 0xFFFFFFFFFFFFFFFF))
        st = w.d(voice + 0x10) if voice else 0
        self.done(iT, st)
        arg6 = self.qret.get("arg6", 0)
        arg7 = self.qret.get("arg7", 0)
        reuse = False
        if st == 1:
            self.emit("~s6d=%d" % self.qret.get(T6D, 0))
            s6f = self.qret.get("s6d_flag", 0)
            if s6f and (b4 & 0x80):
                reuse = True
                self.emit("~s70=%d" % self.qret.get(T70, 0))
                if self.qret.get(T70, 0) == 3:
                    self.emit("~s7a=%d" % self.qret.get(T7A, 0))
                self._set(voice, 0x14, slot, "W14")
                self._set(voice, 0x24, sid, "W24")
                self._set(voice, 0x18, rcpt, "W18")
                if arg6 == 0:
                    self._panvol(voice, pan, vol)
                return      # reuse arm exits at 0x224842: no s78/vt
            else:
                # copy-flag or sd+4 bit7 missing -> 221d60 realloc,
                # then the SAME fresh arm
                self.emit("~a%x" % (elem & 0xFFFFFFFFFFFFFFFF))
                voice = self._alloc(elem)
        # fresh arm: sd+9 byte by sd+4 flags
        nb = 0 if b4 & 0x80 else ((b4 & 1) | 0x40 if b4 & 0x20 else b4)
        self.obs.append((sd + 9, 1, nb))
        self._set(voice, 0x14, slot, "W14")
        self._set(voice, 0x24, sid, "W24")
        self._set(voice, 0x18, rcpt, "W18")
        self._set(voice, 0x10, 1, "W10")
        if arg6 and arg7:
            self._set(voice, 0x2C, 3, "W2c")
            self.emit("~at=%d" % self.qret.get(AT, 0))
            # ~at arm jumps 0x224817: NO pan/vol setters
        else:
            self._set(voice, 0x2C, 2, "W2c")
            self.emit("~ac=%d" % self.qret.get(AC, 0))
            self._panvol(voice, pan, vol)
        self.emit("~s78=%d" % self.qret.get(T78, 0))
        if self.qret.get(T78, 0):
            self._rst(voice)
        self.emit("~vt=0")

    def _rst(self, voice):
        """002256B0 real body: full voice reset (6 field writes)."""
        self.emit("RST%x" % (voice & 0xFFFFFFFFFFFFFFFF))
        self.obs += [(voice + 0x14, 8, 0xFFFFFFFFFFFFFFFF),
                     (voice + 0x1C, 4, 0x7F), (voice + 0x20, 4, 0x40),
                     (voice + 0x24, 4, 0xFFFFFFFF), (voice + 0x28, 4, 0),
                     (voice + 0x10, 4, 2)]

    def m_wsep(self, elem, rcpt, snd_id, pan, vol):
        """00223190: refuse check, sweep, alloc, kind 4/5 attach."""
        w = self.w
        if w.d(elem + 0x30) == 1:
            self._spin(elem)
        b44 = w.b(elem + 0x44)
        if b44 & 0x20:
            ic = self.emit("c")
            self.emit("d")                # 210b30 calls 16d6a0 inside
            self.done(ic, CTX2)
            ix = self.emit("x")
            xr = self._xref()
            self.done(ix, xr)
            if xr:
                return
        self.emit("~o%x" % (elem & 0xFFFFFFFFFFFFFFFF))
        self.emit("~a%x" % (elem & 0xFFFFFFFFFFFFFFFF))
        voice = self._alloc(elem)
        nb = 0 if b44 & 0x80 else ((b44 & 1) | 0x40 if b44 & 0x20 else b44)
        self.obs.append((elem + 0x49, 1, nb))
        self._set(voice, 0x14, 0, "W14")          # xor edx,edx -> slot 0
        self._set(voice, 0x18, rcpt, "W18")
        self._set(voice, 0x10, 1, "W10")
        if self.qret.get("arg6", 0):
            self._set(voice, 0x2C, 5, "W2c")
            self.emit("~at=%d" % self.qret.get(AT, 0))
            # ~at arm jumps 0x2232a3: NO pan/vol setters
        else:
            self._set(voice, 0x2C, 4, "W2c")
            self.emit("~ac=%d" % self.qret.get(AC, 0))
            self._panvol(voice, pan, vol)
        self.emit("~s78=%d" % self.qret.get(T78, 0))
        if self.qret.get(T78, 0):
            self._rst(voice)
        self.emit("~vt=0")

    def _xref(self):
        """210710 returns objA.virtual() or objB.virtual() (al)."""
        g = self.globs
        return 1 if (g.get("xref_a", 0) or g.get("xref_b", 0)) else 0

    # -- shared helpers --
    def _set(self, voice, off, v, tag):
        self.obs.append((voice + off, 8 if v > 0xFFFFFFFF else 4, v))
        self.emit("%s%x" % (tag, voice & 0xFFFFFFFFFFFFFFFF))

    def _tree_lb(self, head, key):
        """00224570's lower_bound: root at head+0x10, node {+0:+8:kids,
        +0x20:key}; returns node or head on miss."""
        w = self.w
        rcx, rdx, rax = w.q(head + 0x10), head, head
        while rcx:
            if w.d(rcx + 0x20) < key:
                rcx = w.q(rcx)
            else:
                rax = rcx
                rcx = w.q(rcx + 8)
        if rax != rdx and key < w.d(rax + 0x20):
            rax = rdx
        return rax

    def _bfind(self, elem, want, off):
        """Prev-chain find from elem+0x10 (last); covers all nodes once."""
        w = self.w
        if w.q(elem + 8) == elem + 8:
            return 0
        node = w.q(elem + 0x10)
        first = w.q(elem + 8)
        while True:
            v = w.q(node + 0x10)
            if v and w.d(v + off) == (want & 0xFFFFFFFF):
                return v
            if node == first:
                return 0
            node = w.q(node + 8)

    def _get_voice(self, elem, slot):
        """221e00: sweeps + find-by-slot; else 221d60 alloc."""
        v = self._bfind(elem, slot, 0x14)
        if v:
            return v
        return self._alloc(elem)

    def _alloc(self, elem):
        """221d60 pool pop -> VOICE; splices LNODE onto elem+8 list."""
        w = self.w
        if w.d(VCTX + 0xA0 + 0x48) == 0:
            return 0
        self.obs.append((VCTX + 0xA0 + 0x48, 4,
                         w.d(VCTX + 0xA0 + 0x48) - 1))
        voice = w.q(FNODE + 0x20)
        # voice ctor obs (2255c0)
        self.obs += [(voice + 0, 8, 0x9087C0), (voice + 8, 8, 0),
                     (voice + 0x10, 4, 0), (voice + 0x14, 8,
                                            0xFFFFFFFFFFFFFFFF),
                     (voice + 0x1C, 4, 0x7F), (voice + 0x20, 4, 0x40),
                     (voice + 0x24, 4, 0xFFFFFFFF), (voice + 0x28, 4, 0)]
        # LNODE splice: {+0:head,+8:prevlast,+0x10:voice}
        prev = w.q(elem + 0x10)
        self.obs += [(LNODE + 0, 8, elem + 8), (LNODE + 8, 8, prev),
                     (LNODE + 0x10, 8, voice),
                     (prev + 0, 8, LNODE) if prev != elem + 8 else
                     (elem + 8, 8, LNODE),
                     (elem + 0x10, 8, LNODE)]
        return voice

    def _panvol(self, voice, pan, vol):
        # 2256f0: NOOP inside (d), carriers 7a7e00/7a7e90 on voice+8,
        # writes voice+0x20 = pan
        ip = self.emit("PAN%x" % (pan & 0xFFFFFFFF))
        self.emit("d")
        self.emit("~se0=%d" % self.qret.get(TE0, 0))
        self.emit("~se9=%d" % self.qret.get(TE9, 0))
        self.done(ip, self.qret.get(TE9, 0))
        self.obs.append((voice + 0x20, 4, pan & 0xFFFFFFFF))
        # 2257e0: eax = vol<0 ? 0 : vol; >=127.0f -> 0x7F; writes +0x1C;
        # tail-jumps 7a81f0 on voice+8
        iv = self.emit("VOL%x" % (vol & 0xFFFFFFFF))
        self.emit("~s81=%d" % self.qret.get(T81, 0))
        self.done(iv, self.qret.get(T81, 0))
        c = s32(vol)
        if c < 0:
            c = 0
        elif c >= 0x7F:
            c = 0x7F
        self.obs.append((voice + 0x1C, 4, c))


def model(case, w):
    m = M(w)
    m.qret = dict(case.get("qret", {}))
    m.globs = case.get("globals", {})
    out = {"trace": m.t}
    ent = case.get("entry", "fork")
    snd_id = case.get("id", 0) & 0xFFFFFFFF
    pan = case.get("pan", 0) & 0xFF
    # the fork masks vol to 0x7f; direct entries pass it raw
    vol = case.get("vol", 0)
    vol = (vol & 0x7F) if ent == "fork" else (vol & 0xFFFFFFFF)
    if ent == "fork":
        sel = case.get("sel", 0)
        if sel == 0:
            rcpt = m.m_seb(w.q(BANK + 8), snd_id, pan, vol)
        else:
            rcpt = m.m_sep(w.q(BANK + 0x10), snd_id, pan, vol)
        out["eax"] = rcpt
    elif ent == "seb":
        out["eax"] = m.m_seb(case.get("sebc", SEBC), snd_id, pan, vol)
    elif ent == "sep":
        out["eax"] = m.m_sep(case.get("sepc", SEPC), snd_id, pan, vol)
    elif ent in ("wseb", "wsebx"):
        m.m_wseb(case.get("elem_p", ELEM), case.get("rcpt_in", 1),
                 snd_id, pan, vol)
    elif ent in ("wsep", "wsepx"):
        m.m_wsep(case.get("elem_p", ELEM2), case.get("rcpt_in", 1),
                 snd_id, pan, vol)
    # last-write-wins at byte granularity: later obs overwrite earlier
    # ones they overlap (ctor/reset qwords vs setter dwords)
    mem = {}
    for a, n, v in m.obs:
        for i in range(n):
            mem[a + i] = (v >> (8 * i)) & 0xFF
    obs = []
    for a in sorted(mem):
        if obs and a == obs[-1][0] + obs[-1][1]:
            obs[-1][2].append(mem[a])
            obs[-1][1] += 1
        else:
            obs.append([a, 1, [mem[a]]])
    out["obs"] = [(a, n, int.from_bytes(bytes(bs), "little"))
                  for a, n, bs in obs]
    return out


def compare(case, world):
    w = Fx(world.planted)
    exp = model(case, w)
    got = " ".join(world.trace)
    expt = " ".join(exp.get("trace", []))
    import re
    norm = lambda s: re.sub(r"[0-9a-f]{6,}", "A", s)
    ok = norm(got) == norm(expt)
    diffs = []
    if not ok:
        diffs.append("trace")
    if "eax" in exp:
        gv = world.uc.reg_read(UC_X86_REG_RAX)
        if s32(gv) != s32(exp["eax"]):
            ok = False
            diffs.append("eax got=%x exp=%x" % (s32(gv), s32(exp["eax"])))
    for addr, n, v in exp.get("obs", []):
        gv = int.from_bytes(world.gm.r(addr, n), "little")
        if gv != v:
            ok = False
            diffs.append("obs %x got=%x exp=%x" % (addr, gv, v))
    if "fault" in exp:
        if not world.faults:
            ok = False
            diffs.append("expected fault, none")
        else:
            faddr = int(world.faults[0][1], 16)
            if faddr != int(exp["fault"], 16):
                ok = False
                diffs.append("fault got=%s exp=%s"
                             % (world.faults[0][1], exp["fault"]))
    elif world.faults:
        ok = False
        diffs.append("faults %s" % world.faults[:2])
    return ok, diffs, got, expt


def build_cases():
    C = []
    def add(name, **kw):
        kw["name"] = name
        C.append(kw)

    V1 = {"voice": {}}

    # ---- FORK (00210C00): selector routing + masking ----------------
    # sel=0 -> Seb; bucket match -> worker runs (visible via obs)
    add("fork-sel0-hit", entry="fork", sel=0, id=0x240, pan=0x40,
        vol=0x7F, seb_elems=[ELEM],
        elem={"bucket": 1, "tnode": {"key": 0x40, "sd": SD},
              "sd": {"b": {4: 0}}},
        voices=V1, voice_alloc=True)
    # sel=0 miss -> receipt still returned, no worker
    add("fork-sel0-miss", entry="fork", sel=0, id=0x240, pan=0x40,
        vol=0x7F, seb_elems=[ELEM], elem={"bucket": 9})
    # sel=1 -> Sep; raw id match
    add("fork-sel1-sep-hit", entry="fork", sel=1, id=0x1234, pan=0x40,
        vol=0x7F, sep_elems=[ELEM2], elem2={"key": 0x1234},
        voices=V1, voice_alloc=True)
    add("fork-sel1-sep-miss", entry="fork", sel=1, id=0x1234, pan=0x40,
        vol=0x7F, sep_elems=[ELEM2], elem2={"key": 0x9999})
    # sel=-1 (nonzero) -> Sep
    add("fork-selneg", entry="fork", sel=0xFFFFFFFF, id=0x1234,
        pan=0x40, vol=0x7F, sep_elems=[ELEM2], elem2={"key": 0x9999})
    # empty lists both sides
    add("fork-sel0-empty", entry="fork", sel=0, id=0x240, pan=0x40,
        vol=0x7F)

    # ---- SEB dispatch (0021B5B0) ------------------------------------
    # negative id: bucket = trunc(id/512) via (id+0x1FF)>>9
    add("seb-neg-bucket", entry="seb", id=0xFFFFFE00, pan=0x40,
        vol=0x7F, seb_elems=[ELEM], elem={"bucket": 0xFFFFFFFF})
    add("seb-neg-bucket2", entry="seb", id=0xFFFFFC00, pan=0x40,
        vol=0x7F, seb_elems=[ELEM], elem={"bucket": 0xFFFFFFFE})
    # two-elem walk, second matches
    add("seb-walk-second", entry="seb", id=0x400, pan=0x40, vol=0x7F,
        seb_elems=[ELEM + 0x4000, ELEM],
        elem={"bucket": 2, "tnode": {"key": 0, "sd": SD},
              "sd": {"b": {4: 0}}},
        objs={ELEM + 0x4000: {"d": {0x3C: 7}}},
        voices=V1, voice_alloc=True)
    # receipt boundary: 0x7FFFFFFE+1 -> 0x7FFFFFFF (mask keeps sign bit
    # clear); also exercises the counter global
    add("seb-rcpt-wrap", entry="seb", id=0x240, pan=0x40, vol=0x7F,
        globals={"rcpt": 0x7FFFFFFE})
    # receipt wrap-to-zero: 0x7FFFFFFF+1 & mask = 0 -> cmove to 1
    add("seb-rcpt-zero", entry="seb", id=0x240, pan=0x40, vol=0x7F,
        globals={"rcpt": 0x7FFFFFFF})

    # ---- SEP dispatch (00219EA0) ------------------------------------
    add("sep-walk-second", entry="sep", id=0x55, pan=0x40, vol=0x7F,
        sep_elems=[ELEM2 + 0x4000, ELEM2],
        elem2={"key": 0x55}, objs={ELEM2 + 0x4000: {"d": {0x38: 0x77}}},
        voices=V1, voice_alloc=True)

    # ---- Seb worker (00224540->00224570 direct) ---------------------
    # fresh arm: tree hit, pool voice state 0 -> W10(1) + kind-2 attach
    # id=0x140: slot &0x1ff=0x140 differs from &0xff=0x40 (m-wseb-slot)
    add("wseb-fresh", entry="wseb", id=0x140, pan=0x40, vol=0x7F,
        rcpt_in=7,
        elem={"tnode": {"key": 0x140, "sd": SD}, "sd": {"b": {4: 0}}},
        voices=V1, voice_alloc=True)
    # reuse arm: voice state 1 + s6d flag + sd+4 bit7 -> stays in reuse
    add("wseb-reuse", entry="wseb", id=0x240, pan=0x40, vol=0x7F,
        rcpt_in=7,
        elem={"tnode": {"key": 0x40, "sd": SD}, "sd": {"b": {4: 0x80}},
              "vlist": ["voice"]},
        voices={"voice": {"d": {0x10: 1, 0x14: 0x40}}},
        qret={"s6d_flag": 1})
    # state!=1 skips the spin loop (mutant m-wseb-state falls in)
    add("wseb-state2", entry="wseb", id=0x140, pan=0x40, vol=0x7F,
        elem={"state": 2})
    # state==1 -> entry+exit spin calls (m-wseb-state discriminator:
    # the mutant compare skips both fences)
    add("wseb-spin", entry="wseb", id=0x240, pan=0x40, vol=0x7F,
        elem={"state": 1, "tnode": {"key": 0x40, "sd": SD},
              "sd": {"b": {4: 0}}},
        voices=V1, voice_alloc=True, qret={"spin_state": 0})
    # tree miss -> silent exit after d
    add("wseb-tree-miss", entry="wseb", id=0x140, pan=0x40, vol=0x7F,
        elem={})
    # s8c bounds fail -> exit
    add("wseb-bounds-fail", entry="wseb", id=0x240, pan=0x40, vol=0x7F,
        elem={"tnode": {"key": 0x40, "sd": SD}, "sd": {"b": {4: 0}}},
        qret={T8C: 0})
    # refuse: sd+4 bit5 -> c + x(1) -> exit
    add("wseb-refuse", entry="wseb", id=0x240, pan=0x40, vol=0x7F,
        elem={"tnode": {"key": 0x40, "sd": SD}, "sd": {"b": {4: 0x20}}},
        globals={"xref_a": 1})
    # sd+4 bit7 in fresh arm -> sd+9 = 0
    add("wseb-flag7", entry="wseb", id=0x240, pan=0x40, vol=0x7F,
        elem={"tnode": {"key": 0x40, "sd": SD}, "sd": {"b": {4: 0x80}}},
        voices=V1, voice_alloc=True)
    # sd+4 bit3 -> ~f2 prev-chain find on voice+0x24; slot==7 skips
    # the found-exit (m-wseb-f2gate / m-wseb-slot7 discriminators)
    add("wseb-flag8", entry="wseb", id=0x207, pan=0x40, vol=0x7F,
        elem={"tnode": {"key": 7, "sd": SD}, "sd": {"b": {4: 8}},
              "vlist": ["voice"]},
        voices={"voice": {"d": {0x10: 1, 0x14: 7, 0x24: 0x80000207}}},
        voice_alloc=True)
    # sd+4 bit5 in fresh arm (refuse passes) -> sd+9 = (0|1)|0x40
    add("wseb-flag5-pass", entry="wseb", id=0x240, pan=0x40, vol=0x7F,
        elem={"tnode": {"key": 0x40, "sd": SD}, "sd": {"b": {4: 0x20}}},
        voices=V1, voice_alloc=True, globals={"xref_a": 0})
    # callback arm: arg6+arg7 -> W2c(3) + ~at (direct entry: the shim
    # zeroes stack args 6/7, so 224570 itself is entered)
    add("wseb-cb-arm", entry="wsebx", id=0x240, pan=0x40, vol=0x7F,
        elem={"tnode": {"key": 0x40, "sd": SD}, "sd": {"b": {4: 0}}},
        voices=V1, voice_alloc=True,
        qret={"arg6": 1, "arg7": 0x12345678})
    # s78 nonzero -> RST resets slot
    add("wseb-s78-rst", entry="wseb", id=0x240, pan=0x40, vol=0x7F,
        elem={"tnode": {"key": 0x40, "sd": SD}, "sd": {"b": {4: 0}}},
        voices=V1, voice_alloc=True, qret={T78: 1})

    # ---- Sep worker (00223160->00223190 direct) ---------------------
    add("wsep-basic", entry="wsep", id=0x55, pan=0x40, vol=0x7F,
        rcpt_in=9, elem2={"flags": 0}, voices=V1, voice_alloc=True)
    add("wsep-refuse", entry="wsep", id=0x55, pan=0x40, vol=0x7F,
        elem2={"flags": 0x20}, globals={"xref_a": 1})
    add("wsep-flag7", entry="wsep", id=0x55, pan=0x40, vol=0x7F,
        elem2={"flags": 0x80}, voices=V1, voice_alloc=True)
    # flags 0x20 (refuse passes) -> elem+0x49 = (0x20&1)|0x40 = 0x40
    add("wsep-flag5-pass", entry="wsep", id=0x55, pan=0x40, vol=0x7F,
        elem2={"flags": 0x20}, voices=V1, voice_alloc=True,
        globals={"xref_a": 0})
    add("wsep-cb-arm", entry="wsepx", id=0x55, pan=0x40, vol=0x7F,
        elem2={"flags": 0}, voices=V1, voice_alloc=True,
        qret={"arg6": 1, "arg7": 0x12345678})
    # volume clamp: raw arg5 vol 0x200 -> 2257E0 clamps to 0x7F
    add("wsep-vol-high", entry="wsepx", id=0x55, pan=0x40, vol=0x200,
        rcpt_in=9, elem2={"flags": 0}, voices=V1, voice_alloc=True)
    return C


def run_case(case, raw, secs):
    world = World(case, raw, secs)
    uc = world.uc
    ent = case.get("entry", "fork")
    entry = {"fork": FORK, "seb": SEB, "sep": SEP,
             "wseb": WSHIM, "wsep": PSHIM,
             "wsebx": WSEB, "wsepx": WSEP}[ent]
    sp = STACK + 0x80000
    uc.reg_write(UC_X86_REG_RSP, sp)
    world.w(sp, qw(RETQ))
    if ent == "fork":
        uc.reg_write(UC_X86_REG_RCX, BANK)
        uc.reg_write(UC_X86_REG_RDX, case.get("sel", 0))
        uc.reg_write(UC_X86_REG_R8, case.get("id", 0))
        uc.reg_write(UC_X86_REG_R9, case.get("pan", 0))
        world.w(sp + 0x28, qw(case.get("vol", 0)))
    elif ent in ("seb", "sep"):
        uc.reg_write(UC_X86_REG_RCX,
                     case.get("sebc", SEBC) if ent == "seb"
                     else case.get("sepc", SEPC))
        uc.reg_write(UC_X86_REG_RDX, case.get("id", 0))
        uc.reg_write(UC_X86_REG_R8, case.get("pan", 0))
        uc.reg_write(UC_X86_REG_R9, case.get("vol", 0))
    elif ent in ("wseb", "wsep"):
        uc.reg_write(UC_X86_REG_RCX,
                     case.get("elem_p", ELEM if ent == "wseb" else ELEM2))
        uc.reg_write(UC_X86_REG_RDX, case.get("rcpt_in", 1))
        uc.reg_write(UC_X86_REG_R8, case.get("id", 0))
        uc.reg_write(UC_X86_REG_R9, case.get("pan", 0))
        world.w(sp + 0x28, qw(case.get("vol", 0)))
    elif ent in ("wsebx", "wsepx"):
        # direct worker entry: arg5/6/7 at entry-rsp+0x28/0x30/0x38
        # (the shims hardcode 6/7 to zero, so the callback arm is only
        # reachable by entering 224570/223190 itself)
        uc.reg_write(UC_X86_REG_RCX,
                     case.get("elem_p", ELEM if ent == "wsebx" else ELEM2))
        uc.reg_write(UC_X86_REG_RDX, case.get("rcpt_in", 1))
        uc.reg_write(UC_X86_REG_R8, case.get("id", 0))
        uc.reg_write(UC_X86_REG_R9, case.get("pan", 0))
        q = case.get("qret", {})
        world.w(sp + 0x28, qw(case.get("vol", 0)))
        world.w(sp + 0x30, qw(q.get("arg6", 0)))
        world.w(sp + 0x38, qw(q.get("arg7", 0)))
    uc.reg_write(UC_X86_REG_RIP, entry)
    try:
        uc.emu_start(entry, RETQ, count=900000)
    except Exception as e:
        world.faults.append(("EMU", str(e),
                             "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
    return world


def build_mutants():
    M = []
    def add(name, va, orig, patch):
        M.append({"name": name, "va": va, "orig": orig, "patch": patch})
    add("m-fork-sel", 0x210C14, b"\x75\x09", b"\x74\x09")      # jne->je
    add("m-fork-vmask", 0x210C0F, b"\x7f", b"\x7e")            # &0x7f->0x7e
    add("m-seb-sar", 0x21B5E1, b"\x09", b"\x08")               # sar 9->8
    add("m-seb-key", 0x21B5FD, b"\x3c", b"\x3d")               # +0x3c->0x3d
    add("m-sep-key", 0x219EDD, b"\x38", b"\x39")               # +0x38->0x39
    add("m-rcal-mask", 0x21295E, b"\xff\xff\xff\x7f",
        b"\xfe\xff\xff\x7f")                                   # mask bits
    add("m-sep-hitgate", 0x219EF3, b"\x74", b"\x75")           # je->jne
    add("m-wseb-slot", 0x2245D5, b"\xff\x01", b"\xff\x00")     # &0x1ff->0xff
    add("m-wseb-state", 0x2245AE, b"\x01", b"\x02")            # state==1->2
    add("m-vol-store", 0x225813, b"\x1c", b"\x1d")             # +0x1c->0x1d
    add("m-wseb-f2gate", 0x22465A, b"\x08", b"\x04")           # sd+4 &8->&4
    add("m-wseb-slot7", 0x224679, b"\x07", b"\x06")            # cmp ebp,7->6
    add("m-wseb-xgate", 0x224687, b"\x20", b"\x10")            # sd+4 &0x20->0x10
    add("m-wseb-freshgate", 0x2246C4, b"\x01", b"\x02")        # state-1->-2
    add("m-wseb-cb6", 0x2247B3, b"\x00", b"\x01")              # arg6 cmp 0->1
    add("m-wseb-kind", 0x2247BC, b"\x03", b"\x02")             # kind 3->2
    add("m-wsep-cb", 0x223249, b"\x00", b"\x01")               # arg6 cmp 0->1
    add("m-wsep-kind", 0x223250, b"\x05", b"\x04")             # kind 5->4
    add("m-wsep-flag", 0x223220, b"\x40", b"\x20")             # |0x40->0x20
    add("m-rcal-zero", 0x212963, b"\x44", b"\x45")             # cmove->cmovne
    return M


MSPEC = {
    "m-fork-sel": "fork-sel1-sep-hit",
    "m-fork-vmask": "fork-sel1-sep-hit",
    "m-seb-sar": "fork-sel0-hit",
    "m-seb-key": "fork-sel0-hit",
    "m-sep-key": "fork-sel1-sep-hit",
    "m-rcal-mask": "seb-rcpt-wrap",
    "m-sep-hitgate": "fork-sel1-sep-hit",
    "m-wseb-slot": "wseb-fresh",
    "m-wseb-state": "wseb-spin",
    "m-vol-store": "wseb-fresh",
    "m-wseb-f2gate": "wseb-flag8",
    "m-wseb-slot7": "wseb-flag8",
    "m-wseb-xgate": "wseb-flag5-pass",
    "m-wseb-freshgate": "wseb-reuse",
    "m-wseb-cb6": "wseb-cb-arm",
    "m-wseb-kind": "wseb-cb-arm",
    "m-wsep-cb": "wsep-cb-arm",
    "m-wsep-kind": "wsep-cb-arm",
    "m-wsep-flag": "wsep-flag5-pass",
    "m-rcal-zero": "seb-rcpt-zero",
}


def main():
    raw, secs = load_image()
    cases = build_cases()
    res = {"exe_sha256": SHA,
           "subjects": {"fork": "0x210C00", "seb": "0x21B5B0",
                        "sep": "0x219EA0", "rcal": "0x212950",
                        "wseb": "0x224570", "wsep": "0x223190"},
           "cases": []}
    npass = 0
    for c in cases:
        world = run_case(c, raw, secs)
        ok, diffs, got_t, exp_t = compare(c, world)
        res["cases"].append({"name": c["name"], "ok": ok,
                             "trace": got_t, "exp": exp_t,
                             "diffs": diffs,
                             "faults": world.faults[:3]})
        if ok:
            npass += 1
        print("CASE %-4s %-22s %s" % ("ok" if ok else "FAIL",
                                      c["name"], got_t[:110]))
        if not ok:
            print("      exp: %s" % exp_t[:110])
            for d in diffs:
                print("      %s" % d)
    print("cases: %d/%d" % (npass, len(cases)))

    nk = 0
    muts = build_mutants()
    for m in muts:
        base = img(raw, secs, m["va"], len(m["orig"]))
        assert base == m["orig"], "%s site bytes %s != %s" % (
            m["name"], base.hex(), m["orig"].hex())
        cname = MSPEC[m["name"]]
        case = dict(next(c for c in cases if c["name"] == cname))
        case["patch_bytes"] = [(m["va"], m["patch"])]
        world = run_case(case, raw, secs)
        ok, diffs, got_t, exp_t = compare(case, world)
        alive = ok
        print("MUT  %-4s %-16s on %-20s %s" % ("ALIVE" if alive else "kill",
              m["name"], cname, got_t[:80]))
        if not alive:
            nk += 1
    print("mutants: %d/%d killed" % (nk, len(muts)))
    res["mutants"] = {"killed": nk, "total": len(muts)}
    res["pass"] = npass == len(cases) and nk == len(muts)
    open("result.json", "w").write(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
